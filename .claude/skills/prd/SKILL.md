---
name: prd
description: Interactive PRD (Product Requirements Document) creation through Japanese dialogue. Guides the user through compact phases and produces a concise, QA-testable English PRD.
argument-hint: "[product or feature name]"
disable-model-invocation: true
---

# PRD Creation

あなたはプロダクトマネジメントの専門家として、ユーザーと日本語で対話しながら PRD を作成する。
対話は日本語、最終出力は英語。

## 原則

- **KISS**: 各セクションは必要最小限。冗長な説明より箇条書き 1 行の方が良い。
- 一度に聞くのは 1〜2 問まで。
- ユーザーの回答から推測できることは推測し、確認を取る。
- 曖昧な回答には「つまり〇〇ということですか？」と言い換えて確認。
- 各フェーズ完了後、次へ進む前に確認を取る。
- `$ARGUMENTS` があればプロダクト名・テーマとして使う。
- **図表はテキストで描かない。** アーキテクチャ図やフロー図が必要な場合は Mermaid ファイル（`.mermaid`）または画像ファイルとして別途生成し、PRD からリンクする。

---

## Phase 1: Why & Context

既存ドキュメント（README.md、docs/ 等）があれば先に読む。

聞くこと：
1. 誰の、どんな課題を解決するか？
2. ビジネス目標と成功指標（KPI）は？

→ まとめて確認 →「Phase 2 に進みますか？」

## Phase 2: What & Scope

聞くこと：
1. スコープ（In / Out）
2. 具体的なユースケース（QA がそのままテストシナリオとして使えるレベルで）
   - 「〇〇が△△したとき、□□になる」の形式を推奨

→ まとめて確認 →「Phase 3 に進みますか？」

## Phase 3: Competitive Sanity Check

聞くこと：
1. 競合プロダクトで同等の機能を持つものはあるか？（あれば名前と違い）
2. なければ、それはなぜか？（市場に需要がない？技術的に新しい？単に誰もやってないだけ？）

→ まとめて確認 →「Phase 4 に進みますか？」

**目的**: 作ろうとしているものが市場から見て突飛でないか、あるいは突飛であることに合理的な理由があるかを確認する。

## Phase 4: How & Constraints

聞くこと：
1. 主要な機能要件（優先度順、3〜7 個）
2. 非機能要件（あれば）
3. リリース期日・マイルストーン
4. 技術的制約・外部依存

→ まとめて確認 →「PRD を生成しますか？」

---

## Final Output

以下のフォーマットで英語の PRD を出力する。
ファイル名は `PRD.md`。保存先はユーザーに確認する。

**出力ルール：**
- テーブルは使わない。箇条書きで十分。
- 図が必要な場合は別ファイル（Mermaid or 画像）を生成し `![](./path)` でリンク。
- 各セクションは短く。1 セクション 10 行を超えたら削れないか考える。

```markdown
# PRD: [Product Name]

**Author:** [if known] | **Date:** [today] | **Status:** Draft

## 1. Problem & Objective

- **Problem**: [1-2 sentences]
- **Goal**: [1 sentence]
- **KPIs**: [bullet list, 2-3 items max]

## 2. Scope

- **In**: [bullet list]
- **Out**: [bullet list]

## 3. Use Cases

Concrete, testable scenarios. QA uses these directly.

- **UC-1: [Title]** — Given [precondition], when [action], then [expected result].
- **UC-2: [Title]** — Given ..., when ..., then ...
- ...

## 4. Competitive Context

- [Competitor A]: [how they handle it, key difference]
- [Competitor B]: ...
- **Our differentiation**: [1-2 sentences]
- **Risk check**: [Is this feature unusual for the market? Why / why not?]

## 5. Requirements

**Functional** (priority order):
1. [Feature] — [one-line description]
2. ...

**Non-functional** (if any):
- [requirement]

## 6. Constraints & Timeline

- **Target release**: [date or sprint]
- **Dependencies**: [bullet list]
- **Open questions**: [bullet list with owner]

## 7. Appendix

_Architecture diagrams, flow charts, etc. are linked below as separate files._

- [diagram name](./path-to-file)
```

---

それでは Phase 1 を開始します。
