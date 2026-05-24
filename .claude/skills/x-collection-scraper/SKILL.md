---
name: x-collection-scraper
description: X(Twitter)の任意コレクション(likes/bookmarks/user posts等)から投稿本文・著者・URL・(任意で)画像OCR結果を抽出し、Markdownファイルとしてダウンロードする。広告は除外、本文は全文そのまま、できる限り全件取得。
---

# X(Twitter) コレクション → Markdown 抽出

## 用途
X(Twitter) の任意コレクションページ (likes / bookmarks / user posts / replies / media) から、投稿本文・著者・URL・(任意で)画像OCRを抽出し、Markdownファイルとしてダウンロードする。

## 入力パラメータ
- `targetUrl`: 抽出対象ページ (例: `https://x.com/{handle}/likes`, `https://x.com/i/bookmarks`)
- `outputFilename`: 出力ファイル名 (例: `koheionod-likes.md`)
- `ocrImages`: 画像OCRを行うか (true/false)。bookmarks で有用
- `excludeAds`: 広告除外 (デフォルト true)

## ルール (MUST)
- 広告は除外する (`User-Name` 内に "Ad" / "広告" の span を含むものを検出)
- 本文は **全文そのまま** (要約禁止)
- できる限り **全件** (スクロールで末尾まで)
- ダウンロード前に **ユーザー承認** を取る
- 初回タスクは **2〜3件プレビュー → 承認 → 全件実行**

## 標準ワークフロー

### Step 1: プラン提示
`update_plan` で以下を提示:
- domains: `x.com`, `pbs.twimg.com`, OCR時は `cdn.jsdelivr.net`
- approach: scroll-collect → dedupe → markdown → download

### Step 2: スクロール収集ループ
対象タブで以下を実行する。

```js
// === X collection scraper ===
window.__collected = window.__collected || new Map(); // key=postURL
window.__imgs = window.__imgs || new Map();           // key=postURL, val=Set<imgURL>
window.__stagnant = 0;

window.__collectOnce = () => {
  document.querySelectorAll('article[data-testid="tweet"]').forEach(a => {
    // 広告除外
    const userNameBlock = a.querySelector('[data-testid="User-Name"]');
    if (!userNameBlock) return;
    const labelTexts = [...a.querySelectorAll('span')].map(s => s.textContent);
    if (labelTexts.includes('Ad') || labelTexts.includes('広告')) return;

    // URL
    const link = a.querySelector('a[href*="/status/"]');
    if (!link) return;
    const url = 'https://x.com' + link.getAttribute('href').split('?')[0];

    // 著者
    const nameSpans = userNameBlock.querySelectorAll('span');
    const displayName = nameSpans[0]?.textContent || '';
    const handle = [...nameSpans].map(s=>s.textContent).find(t => t.startsWith('@')) || '';

    // 本文
    const textEl = a.querySelector('[data-testid="tweetText"]');
    const text = textEl ? textEl.innerText : '';

    if (!window.__collected.has(url)) {
      window.__collected.set(url, { displayName, handle, text, url });
    }

    // 画像 (OCR用)
    if (!window.__imgs.has(url)) window.__imgs.set(url, new Set());
    a.querySelectorAll('img[src*="pbs.twimg.com/media"]').forEach(img => {
      const hi = img.src.replace(/&name=\w+/, '&name=large');
      window.__imgs.get(url).add(hi);
    });
  });
  return window.__collected.size;
};

// スクロールループ (X の仮想スクロール対策: 小刻みに進める)
window.__scrollLoop = async (maxIter=400) => {
  let prev = 0;
  for (let i=0; i<maxIter; i++) {
    window.__collectOnce();
    window.scrollBy(0, window.innerHeight * 0.55);
    await new Promise(r => setTimeout(r, 1500));
    if (window.__collected.size === prev) {
      window.__stagnant++;
      if (window.__stagnant >= 8) break;
    } else {
      window.__stagnant = 0;
    }
    prev = window.__collected.size;
  }
  return window.__collected.size;
};
window.__scrollLoop();
```

数回に分けてポーリング (`window.__collected.size` 確認)。停滞 8 回で終了。

### Step 3: (任意) 画像OCR
X.com の CSP で外部スクリプトがブロックされるため、**別タブで `cdn.jsdelivr.net/npm/tesseract.js@5/` を開き**、そこで OCR を実行する。

```js
// === OCR tab 側 ===
// 1. Tesseract をロード
const s = document.createElement('script');
s.src = 'https://cdn.jsdelivr.net/npm/tesseract.js@5/dist/tesseract.min.js';
document.head.appendChild(s);

// 2. ロード後、OCR ヘルパを定義
window.__ocr = async (imgUrl) => {
  const r = await Tesseract.recognize(imgUrl, 'jpn+eng');
  return r.data.text;
};

// 3. X タブから window.__imgs を JSON 文字列で手動転送 (チャンク化)
//    → window.__bmJsonStr に連結 → JSON.parse して使う
// 4. 並列 OCR (Promise.all、ただし長時間は fire-and-forget + 後追いポーリング)
```

### Step 4: text-main 判定ヒューリスティック (v2)
```js
function isTextMainV2(t) {
  const cleaned = t.replace(/\s+/g, '');
  if (cleaned.length < 50) return false;
  const longEng = (t.match(/[A-Za-z]{5,}/g) || []).length;
  const longJp  = (t.match(/[ぁ-んァ-ヴー一-龯]{4,}/g) || []).length;
  const totalSignal = longEng + longJp;
  const chunks = t.split(/\s+/).filter(Boolean).length || 1;
  const ratio = totalSignal / chunks;
  return totalSignal >= 8 && ratio >= 0.15;
}
```
これ未満は「写真等」と分類する。

### Step 5: Markdown 生成
```js
window.__full = [...window.__collected.values()].map((p, i) => {
  const imgs = [...(window.__imgs.get(p.url) || [])];
  let imgBlock = '';
  if (imgs.length) {
    imgBlock = '\n\n**画像 (' + imgs.length + '枚):**\n' + imgs.map((u, j) => {
      const ocr = window.__ocrResults?.[u];
      if (ocr && isTextMainV2(ocr)) {
        return '- 画像' + (j+1) + ' (テキストメイン - OCR抽出):\n\`\`\`\n' + ocr.trim() + '\n\`\`\`';
      }
      return '- 画像' + (j+1) + ': (テキストメインではない / 写真等)';
    }).join('\n');
  }
  return '## ' + (i+1) + '. ' + p.displayName + ' (' + p.handle + ')\nURL: ' + p.url + '\n\n**本文:**\n' + p.text + imgBlock + '\n\n---\n';
}).join('\n');
```

### Step 6: ダウンロード (ユーザー承認後)
```js
const blob = new Blob([window.__full], {type: 'text/markdown'});
const a = document.createElement('a');
a.href = URL.createObjectURL(blob);
a.download = 'koheionod-bookmarks.md'; // 適宜変更
a.click();
```

## 既知の落とし穴と回避策

| 問題 | 回避策 |
|---|---|
| X の仮想スクロールで DOM から消える | スクロール幅を小さく (0.5〜0.6 × viewport)、待機 1500ms |
| 同 → 画像URLが取れない投稿が出る | 収集を多パス化 (`window.__imgs` を Map で蓄積) |
| X.com の CSP で外部 JS ブロック | OCR は別タブ (jsdelivr) で実行 |
| ツール出力が 1500〜2000 字で truncate | クエリを 3〜5 項目ずつに分割 |
| "BLOCKED: Cookie/query string data" | 大きい文字列を slice して小分けに返す |
| OCR 45 秒で CDP タイムアウト | fire-and-forget + 後追いポーリング |
| 画像IDの偶発衝突 (X Article 形式) | 該当投稿は個別に開き Article 本文を取得 (本文 + 先頭500字で代替) |
| 広告混入 | `User-Name` 内に "Ad" / "広告" の span を含むものを除外 |

## 出力フォーマット
```
## N. DisplayName (@handle)
URL: https://x.com/...

**本文:**
[全文そのまま]

**画像 (N枚):**
- 画像1 (テキストメイン - OCR抽出):
  \`\`\`
  [OCR結果]
  \`\`\`
- 画像2: (テキストメインではない / 写真等)

---
```

## 実績
- `koheionod/likes`: 163 件 / 31.5KB
- `i/bookmarks`: 19 件 / 12KB (画像 21 枚 OCR、うち text-main 判定 7 枚)
