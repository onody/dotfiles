---
name: finance
description: クレカ・銀行・株の取引ログや残高スクショを受け取り、/Users/onod/src/memo の raw/finance/ 台帳（transactions.tsv, stocks.tsv, balances.tsv）に正規化して追記する。Use when the user shares カード明細/銀行明細/証券取引履歴/残高 (Amex, 楽天カード, 楽天銀行, 証券会社の約定履歴など) as PDF/CSV/スクショ/コピペ, or says "家計簿に取り込んで", "financeに追加して", "この明細を整形して保存して".
---

# finance

`/Users/onod/src/memo/raw/finance/` の家計台帳を更新するskill。パーサースクリプトは持たず、渡されたログをClaudeが直接読んで正規化・追記する。

## 対象ファイル

- `raw/finance/transactions.tsv`: クレカ・銀行の入出金（縦持ち、1行=1取引）
- `raw/finance/stocks.tsv`: 株・証券の売買履歴
- `raw/finance/balances.tsv`: 口座残高のスナップショット
- `raw/finance/categories.md`: 支出カテゴリのキーワード辞書

## Amazon注文履歴による補完（Your Orders / Request My Data）

Amazonの「データのリクエスト」でダウンロードできる `Your Orders` フォルダ（`Retail.OrderHistory.3/Retail.OrderHistory.3.csv` を含む）が渡された場合は、新規取引としてではなく、**既存のAmex `アマゾン ＪＰ マーケットプレイス` 行の `memo` 列を商品名で補完する**用途にのみ使う。

方針:
- Amazon注文データを新規行として `transactions.tsv` に追加しない（同じ支払いがAmex側で既に記帳されているため二重計上になる）
- 既存行の `description` は絶対に書き換えない（`description` は重複除外キーに含まれるため、書き換えると次回以降の同期間の再取り込みで重複判定が壊れる）
- 書き換えて良いのは `memo` 列のみ（重複除外キーに含まれず、金額・カテゴリ集計にも影響しないため）
- 対象は `description` が完全一致で `アマゾン ＪＰ マーケットプレイス` の行のみ（`アマゾンサービシーズインターナショナル` はKindle等のデジタル注文で、Amazon側のエクスポートにカード情報が付かず安全にマッチできないため対象外）

マッチング手順:
1. `Retail.OrderHistory.3.csv` の `Payment Instrument Type` から `AmericanExpress - XXXX`（下4桁）を抽出する
2. `transactions.tsv` の既存amex `account`（例: `-82000`）の下4桁と突き合わせ、対応するカードを特定する
3. 同じ `(account, Ship Date のJST日付, Order ID)` でグループ化し `Total Owed` を合算する（同一注文が複数配送に分かれる場合は配送ごとに分離される）
4. 各Amexの対象行について、`account` と `amount` が一致し、`date` とグループのJST日付の差が±2日以内のグループを探す
5. 候補が一意に定まる場合のみ採用する。Amex側に同一 `(date, account, description, amount)` の行が複数ある場合、またはAmazon側の候補グループが複数ある場合は、**両方ともスキップ**して件数を報告する（推測で割り当てない）
6. 採用した行は `memo` に商品名を追記する（既存memoがあれば `/` で連結。複数商品の場合は `、` で連結し、同一商品が複数個ある場合は `×n` を付ける）

出力時は通常の報告に加えて、Amazon補完のマッチ件数・未マッチ件数・スキップ件数（曖昧で判定不能だった件数）も報告する。

## 基本方針

- 対象は必ず `/Users/onod/src/memo` のメインリポジトリ
- 該当ファイルに直接追記する。既存行は書き換えない（重複除外のみ行う）
- グラフ化を前提にしたフォーマットなので、列を勝手に増やしたり日本語列名にしたりしない
- 迷ったら自動判断より報告を優先する
- 個人情報（カード番号のフル桁など）はそのまま書き込まない。マスクされた形式のまま扱う

## 手順

### 1. 入力を判定する

渡された内容が以下のどれかを判定する。複数種類が混ざっている場合はそれぞれ該当ファイルに振り分ける。

- クレカ明細 → `transactions.tsv`
- 銀行口座の入出金明細 → `transactions.tsv`
- 株・証券の約定履歴 → `stocks.tsv`
- 口座残高のスクショ・一覧 → `balances.tsv`

### 2. transactions.tsv への追記

列: `date, posted_date, source, account, holder, description, amount, direction, category, memo`

- `date`: 取引日 (YYYY-MM-DD)
- `posted_date`: 反映日・請求確定日。なければ空
- `source`: `amex` / `rakuten_card` / `rakuten_bank` など、サービスを表す短い英語スラッグ。初出のサービスは適当な新しいスラッグを作ってよい
- `account`: 口座・カード番号の識別子（マスク済みでよい）
- `holder`: 名義人。不明なら空
- `description`: 明細本文をそのまま（全角/半角の乱れはそのままでよい、無理に正規化しない）
- `amount`: 金額。常に正の整数
- `direction`: `expense` / `income` / `transfer`
- `category`: `categories.md` を読み、キーワードに部分一致するカテゴリを機械的に割り当てる。上から順に評価し最初に一致したものを採用、一致しなければ `未分類`。`direction` が `income` なら常に `収入`、`transfer` なら常に `振替`
- `memo`: 支払方法など補足（`card`, `1回払い` 等）。なければ空

新しい店名・サービスが `未分類` になり、今後も出てきそうなら `categories.md` にキーワードを追記する（辞書は育てるもの。都度Claudeが判断して埋める）。

### 3. stocks.tsv への追記

列: `date, source, account, action, symbol, quantity, price, amount, currency, memo`

- `action`: `buy` / `sell` / `dividend` / `fee` / `interest` / `deposit` / `withdrawal`（`deposit`/`withdrawal`は証券口座への入出金。積立入金・クイック入金なども`deposit`にまとめる）
- `symbol`: 銘柄名またはティッカー
- `quantity` / `price`: 配当や手数料など株数・単価が関係ない行は空にする
- `amount`: 合計金額。手数料込みかどうかは `memo` に書く
- `currency`: `JPY` / `USD` など

### 4. balances.tsv への追記

列: `date, source, account, balance, currency, memo`

残高はその時点のスナップショットとして追記する。上書きせず、日付ごとに行を積む。

### 5. 重複除外

追記前に、追記先ファイルの既存行と以下が完全一致する行がないか確認する。一致すれば追記しない。

- `transactions.tsv`: `(date, posted_date, source, account, description, amount, direction)`
- `stocks.tsv`: `(date, source, account, action, symbol, quantity, price, amount)`
- `balances.tsv`: `(date, source, account, balance)`

`category`/`memo`/`holder` は判定に使わない（表記ゆれや後からの追記で変わりうるため）。

注意: `date`・`source`・`account`・`amount` だけで判定すると、同日同額の別取引（返金と再購入のペア、同じ店で同額の買い物を2回など）を誤って重複扱いしてしまう。実際に過去データでこのパターンが複数件見つかっている。`direction`（返金/再購入の区別）と `posted_date`（別日の別注文の区別）を必ず鍵に含めること。

### 6. 出力

作業完了時は短く報告する:
- 追記した件数（ファイルごと）
- `未分類` になった件数と主な内訳
- 重複としてスキップした件数
- `categories.md` に追記した場合はその内容

## 注意

- `raw/finance/.gitignore` は `transactions.tsv` `stocks.tsv` `balances.tsv` `categories.md` `.gitignore` 以外を無視する設定にしてある。ダウンロードした生のPDF/CSV自体はコミット対象に含めない
- コミットするかどうかは明示的に指示されない限りこのskill側では判断しない（追記のみ行い、commit/pushはユーザー指示があれば別途行う）
