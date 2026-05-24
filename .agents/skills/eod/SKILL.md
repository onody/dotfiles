---
name: eod
description: memo リポジトリの EOD(end of day) ルーティンを実行する。Use when the user says "eod", "EOD", "終業処理", "一日の終わりのルーティン", or asks to run the end-of-day workflow for /Users/onod/src/memo.
---

# EOD

`/Users/onod/src/memo` 用の終業ルーティン。

## 基本方針

- すべて ` /Users/onod/src/memo ` のメインリポジトリを対象にする
- worktree 内で動いていても、操作対象は必ずメインリポジトリに固定する
- 迷ったら自動修正より報告を優先する
- 変更対象は原則 `raw/` と `wiki/` のみ
- EOD 専用スクリプトは skill の一部として ` /Users/onod/.agents/skills/eod/scripts/ ` に置く

## 承認まわり

- Step 1〜4 は通常そのまま実行してよい
- 承認が要るのは基本的に Git の更新系だけ
- 毎回 `git add` `git commit` `git push` を個別に叩くのはだるいので、Step 5 は固定スクリプト ` /Users/onod/.agents/skills/eod/scripts/eod_finalize.sh ` を使う
- Codex の権限制約上、skill だけで承認を完全に消すことはできない
- ただし、この固定スクリプト実行に対する prefix 承認が一度通っていれば、以後の EOD は承認なしで最後まで流せる

## 手順

### 1. ファイル名の精査

確認対象:
- `/Users/onod/src/memo/raw/`
- `/Users/onod/src/memo/raw/diary/`
- `/Users/onod/src/memo/raw/clipping/`
- `/Users/onod/src/memo/raw/training/`

ルール:
- `raw/` 直下の `YYYY-MM-DD.md` は `raw/diary/` に移動する
- `raw/` 直下の `training-YYYY-MM.md` は `raw/training/YYYY-MM.md` に移動する
- `raw/clipping/` のファイル名は `english-lowercase-kebab-case.md` に正規化する
- clipping をリネームしたら、`raw/diary/` 内の `[[旧名]]` と `[[旧名|...]]` を新ファイル名に追従させる
- `raw/` 直下のその他ファイルは `english-lowercase-kebab-case.md` か確認し、違反は報告する。勝手に直さない

clipping の正規化:
- スペースは `-`
- 英大文字は小文字化
- 記号は除去
- 拡張子は `.md` を維持

### 2. リンクの精査

対象:
- `/Users/onod/src/memo/wiki/`
- `/Users/onod/src/memo/raw/diary/`

やること:
- すべての `[[リンク]]` を収集する
- リンク先ファイル名と、`raw/` 配下または `wiki/` 配下の実ファイル名を拡張子なしで照合する
- 壊れたリンクを報告する
- 明らかに直せるものだけ修正する

### 3. 当日の会話ログから洞察を拾う

今日の Claude 会話ログを `~/.claude/projects/-Users-onod-src-memo/*.jsonl` から読む。

加えて、Codex / ChatGPT Desktop 側も読む:

```bash
python3 /Users/onod/.agents/skills/eod/scripts/eod_collect_codex_history.py
```

これは `~/.dotfiles/.codex/history.jsonl` と `~/.dotfiles/.codex/state_5.sqlite` を使い、`/Users/onod/src/memo` を対象にした当日の Codex ユーザー発話だけを拾う。

注意:
- Claude 側は user / assistant の両方を見られる
- Codex 側は現状、安定して取れるのはユーザー発話だけ
- `Library/Application Support/com.openai.chat` に会話データはあるが、素直なテキストとしては扱いにくい。EOD では無理に掘らず、Codex はユーザー発話を一次ソースとして扱う

抽出対象:
- 事実
- 学び
- 意思決定
- 新しい知識
- 方針変更

除外対象:
- 単なるツール操作
- ファイル確認
- コード編集の作業ログ
- 雑談
- この EOD 実行そのもの

wiki に反映する価値があるものだけ残す。

出典:
- Claude 由来: `> [source: claude-session YYYY-MM-DD]`
- Codex 由来: `> [source: codex-session YYYY-MM-DD]`

### 4. Ingest

対象ソースは次で決める:

1. `git -C /Users/onod/src/memo diff --name-only HEAD`
2. `git -C /Users/onod/src/memo ls-files --others --exclude-standard raw/`
3. Step 3 で拾った会話ログの洞察

進め方:
- 対象ソースを読む
- `wiki/schema.md` を読んで、更新すべき wiki ページを判断する
- `raw/diary/YYYY-MM-DD.md` からは、事実・観察・学び・決定事項だけを反映する
- 感情や愚痴は wiki に入れない
- 既存方針と矛盾する内容は消さずに `> ⚠️ 要確認:` で残す
- 1 回の ingest で更新する wiki ページは最大 5 ページ
- 更新したページの `最終更新:` は今日の日付にする

### 5. Git

最後は固定スクリプトで実行する:

```bash
/Users/onod/.agents/skills/eod/scripts/eod_finalize.sh
```

このスクリプトは commit 前に、今回変更が入った `raw/` と `wiki/` 配下の Markdown だけを正規化する。

正規化ルール:
- 行末の半角スペース・タブを削除
- 連続空行は 1 行に圧縮
- 末尾の余計な空行を削除
- ファイル末尾は必ず 1 個の改行で終える

制約:
- `.claude/worktrees/` は絶対にステージしない
- コミットメッセージはスクリプト側で必ず `EOD YYYY-MM-DD`
- `raw/` と `wiki/` 以外はステージしない
- 差分がなければ空コミットは作らず終了する

## 出力

完了時は短く報告する:
- 更新した wiki ページ一覧
- 変更の要約
- 自動修正できなかった問題

## 注意

- リポジトリが dirty でも、EOD に無関係な変更は巻き込まない
- 壊れたリンクや曖昧な rename は、無理に直して壊すより報告
- push まで含むので、実行前に未確認の大きな変更がないか一度見る
