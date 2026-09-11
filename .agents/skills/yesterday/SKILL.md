---
name: yesterday
description: memo リポジトリの前日分ラップアップ(旧EOD)ルーティンを実行する。Use when the user says "yesterday", "昨日の分", "前日分", "前日のwiki反映", "yesterdayを実行して", or asks to process the previous day's notes for /Users/onod/src/memo.
---

# yesterday

`/Users/onod/src/memo` 用の、前日分をwikiに反映するルーティン（旧名 `eod`）。

## 対象日

- デフォルトの対象日は常に「前日」（JST）。このルーティンは翌朝に実行する運用のため、当日ではなく前日分を扱う
- auto-diary の `summarize`（Mac起動時、前日分のOCRサマリ生成）から自動起動された場合は、プロンプトに対象日（前日の日付、YYYY-MM-DD）が明示される。この場合はその対象日をそのまま使う
  - Step 3 の `yesterday_finalize.sh <対象日>` の引数、コミットメッセージの日付に反映する
  - `raw/diary/YYYY-MM-DD.auto.md` は対象日と同じ日付のものを優先して読む
- ユーザーが明示的に別の日付を指定した場合（例:「6/20分をやって」）はその日付を対象日とする

## 基本方針

- すべて ` /Users/onod/src/memo ` のメインリポジトリを対象にする
- worktree 内で動いていても、操作対象は必ずメインリポジトリに固定する
- 迷ったら自動修正より報告を優先する
- 変更対象は原則 `raw/` と `wiki/` のみ
- 専用スクリプトは skill の一部として ` /Users/onod/.agents/skills/yesterday/scripts/ ` に置く

## 承認まわり

- Step 1〜3 は通常そのまま実行してよい
- 実行時はユーザーに承認や許可を求めない
- 毎回 `git add` `git commit` `git push` を個別に叩くのはだるいので、Step 3 は固定スクリプト ` /Users/onod/.agents/skills/yesterday/scripts/yesterday_finalize.sh ` を使う
- 既知のコマンドや保存済み prefix 承認が使える場合は、そのまま実行する
- Codex の実行環境が外部制約で止めた場合でも、モデル側からユーザーに確認を求めず、まず既存の承認済み経路で完結できるかを優先して試す
- Step 3 の失敗原因が `PATH` や `python3` `git` `ssh` などの実行環境差分なら、その場しのぎの一時ラッパーより先に `yesterday_finalize.sh` 自体を直して恒久化する

## 手順

### 1. ファイル名整理・リンク検証

固定スクリプトで一括実行する（従来 Step1〜2 で ls/mv/grep を8〜10回に分けて叩いていたのを1回にまとめたもの）:

```bash
python3 /Users/onod/.agents/skills/yesterday/scripts/yesterday_precheck.py
```

このスクリプトが自動で行うこと（機械的に安全な操作のみ）:
- `raw/` 直下の `YYYY-MM-DD.md` を `raw/diary/` に移動
- `raw/` 直下の `training-YYYY-MM.md` を `raw/training/YYYY-MM.md` に移動
- `raw/clipping/` のファイル名を `english-lowercase-kebab-case.md` に正規化（スペース→`-`、大文字→小文字、記号除去）し、リネームに伴う `raw/diary/` 内の `[[旧名]]` `[[旧名|...]]` 参照も自動で新名に書き換える

スクリプトが自動修正せず「要判断」として報告するだけのもの（ここは迷ったら報告を優先する方針通り、エージェント側で個別に判断する）:
- kebab-case化しても非ASCII文字などが残り正規化しきれない clipping ファイル名
- `raw/` 直下のその他ファイルの命名違反（勝手に直さない）
- `wiki/` と `raw/diary/` 内の `[[リンク]]` のうち、リンク先が見つからないもの（明らかに直せるものだけ手動で修正し、迷うものは報告に留める）

### 2. Ingest

対象ソースは次で決める:

1. `git -C /Users/onod/src/memo diff --name-only HEAD`
2. `git -C /Users/onod/src/memo ls-files --others --exclude-standard raw/`
3. 対象日または直近で更新された `raw/diary/YYYY-MM-DD.auto.md`（auto-diary による画面活動サマリ）

進め方:
- 対象ソースを読む
- `wiki/schema.md` を読んで、更新すべき wiki ページを判断する
- `wiki/places.md` を更新する必要がありそうなら、先に次を実行して URL から店名・地名を補完する

```bash
python3 /Users/onod/.agents/skills/yesterday/scripts/yesterday_sync_places.py
```

- `raw/diary/YYYY-MM-DD.md` からは、事実・観察・学び・決定事項だけを反映する
- `raw/diary/YYYY-MM-DD.auto.md` からも同様に、事実・観察・学び・決定事項だけを反映する。UI 断片や生ログは除外する
- auto-diary 由来の反映には `> [source: auto-diary YYYY-MM-DD]` を付与する
- `wiki/places.md` については、日記内の `行きたい` `行ってみたい` `食べたい` `泊まりたい` などの具体候補も拾う
- 候補が URL しか持っていなくても捨てず、`未整理` の行として一旦残す
- URL-only の候補は、後で店名や場所が判明したら既存行を正規化して置き換える
- 感情や愚痴は wiki に入れない
- 既存方針と矛盾する内容は消さずに `> ⚠️ 要確認:` で残す
- 1 回の ingest で更新する wiki ページは最大 5 ページ
- 更新したページの `最終更新:` は対象日の日付にする

### 3. Git

最後は固定スクリプトで実行する:

```bash
/Users/onod/.agents/skills/yesterday/scripts/yesterday_finalize.sh [対象日]
```

引数を省略すると前日の日付でコミットする。auto-diary からの自動起動時は対象日を渡す。

このスクリプトは commit 前に、今回変更が入った `raw/` と `wiki/` 配下の Markdown だけを正規化する。

前提:
- `yesterday_finalize.sh` は Codex の制限環境でも単体で完走できる状態を保つ
- 具体的には、スクリプト内で標準的な `PATH` を bootstrap し、`python3` `git` `ssh` を自前で解決する
- ad-hoc な `/tmp` コピーや一時置換は恒久対応ではない。必要なら script を修正してから再実行する

正規化ルール:
- 行末の半角スペース・タブを削除
- 連続空行は 1 行に圧縮
- 末尾の余計な空行を削除
- ファイル末尾は必ず 1 個の改行で終える

制約:
- `.claude/worktrees/` は絶対にステージしない
- コミットメッセージはスクリプト側で必ず `EOD YYYY-MM-DD`（過去の commit history との継続性のため、コミットメッセージのプレフィックスだけは旧名を維持する）
- `raw/` と `wiki/` 以外はステージしない
- 差分がなければ空コミットは作らず終了する
- 実行中、この Step についてユーザーへ承認確認メッセージを出さない

## 出力

完了時は短く報告する:
- 更新した wiki ページ一覧
- 変更の要約
- 自動修正できなかった問題

## 注意

- リポジトリが dirty でも、このルーティンに無関係な変更は巻き込まない
- 壊れたリンクや曖昧な rename は、無理に直して壊すより報告
- push まで含むので、実行前に未確認の大きな変更がないか一度見る
