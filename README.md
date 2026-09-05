# 自律と自己陶冶

**自分の生をどこまで自分で治められるか**を主題にした、二篇のプレプリントを収めたリポジトリです。

一篇は独身（celibacy）を、性的活動の欠落ではなく擁護しうる自己陶冶の型として読み直します。
もう一篇は、断片化した自己を統合する試みを「人格的帝国主義」という概念のもとで素描します。
主題は離れて見えますが、問いは共通しています —— **何を基準に、自分の生の形を決めるのか**。

どちらも査読前の原稿です。著者による公開は SSRN・PhilArchive などの窓口で行っており、
このリポジトリは**全文を読める形に開き、版と出典をひとところに置くため**のものです。

**読みやすい形の公開版** → [cpsbvbng26-dotcom.github.io/autonomy-and-self-cultivation](https://cpsbvbng26-dotcom.github.io/autonomy-and-self-cultivation/)

## 二篇

### [The Nobility and Exemplarity of the Celibate Individual](papers/celibate-individual.md)

*An Antinatalist and Ascetic Reconsideration of Autonomy and Quality of Life* — v2, 2026年8月22日

性的活動を倫理的に必要とみなす通説は、生殖がなければ社会は存続しないという事実から個人の義務を
導いています。この論文は、その移行が反出生主義の議論を前に持ちこたえないことを示したうえで、
エピクロスの快の区別とショーペンハウアーの意志の形而上学を手がかりに、他者や欲望の周期に
依存しない自足的な幸福という観点から独身を積極的に評価します。

[全文](papers/celibate-individual.md) ｜ [PDF](pdf/nobility-and-exemplarity-of-the-celibate-individual-v2.pdf)

### [Manifesto of Imperial Selfhood](papers/imperial-selfhood.md)

*An Exploratory Essay on Personal Imperialism and Spiritual Sovereignty* — 改訂版, 2026年8月

カントの「目的の王国」から立法の層を、ニーチェの力への意志から評価の層を、ユンガーの
「労働者のゲシュタルト」から動員の層を取り、三層構造として組み立てます。眼目は、三者を
滑らかに統合しないところにあります —— 普遍主義と遠近法主義の緊張こそが構造の中身である、と論じます。

[全文](papers/imperial-selfhood.md) ｜ [PDF](pdf/manifesto-of-imperial-selfhood-revised.pdf)

## このリポジトリの構成

| | |
| --- | --- |
| [papers/](papers/README.md) | 全文（Markdown）。PDF の本文を起こしたもの |
| [pdf/](https://github.com/cpsbvbng26-dotcom/autonomy-and-self-cultivation/tree/main/pdf) | 配布した PDF そのもの |
| [docs/how-to-cite.md](docs/how-to-cite.md) | 引用の書き方 |
| [docs/ai-disclosure.md](docs/ai-disclosure.md) | 執筆における AI 利用の開示 |
| `build.js` | Markdown を静的な HTML に変換する（依存パッケージなし） |

### なぜ Markdown も置くのか

PDF は体裁を固定できますが、本文を引用しようとすると行が割れ、検索にもかかりにくく、
版のあいだの違いも見えません。同じ本文を Markdown でも置いておくと、節の見出しに直接リンクでき、
`git diff` で改訂の中身がそのまま読め、全文検索も効きます。**PDF が配布物、Markdown が読むための形**、
という役割分担です。

本文は PDF から起こしたもので、書き写したものではありません。抽出した語の並びと照合して、
独身論は全 3739 語が一致、人格的帝国主義は全 4368 語のうち 4 語が異なります。この 4 語は
`non-negotiable` `self-overcoming` のように**行末で割れたハイフン語を繋ぎ直した箇所**で、
それ以外に手を入れた箇所はありません。

日本語の要旨だけは、このリポジトリのために書き下ろしたもので、原文にはありません。

## 公開先

著者ページは次のとおりです。各論文の掲載ページと内容が食い違う場合は、掲載ページを正とします。

| | |
| --- | --- |
| SSRN | [著者ページ](https://papers.ssrn.com/sol3/cf_dev/AbsByAuth.cfm?per_id=8730280) |
| PhilPeople / PhilArchive | [著者ページ](https://philpeople.org/profiles/takuyanemoto) |
| ORCID | [0009-0000-1406-0547](https://orcid.org/0009-0000-1406-0547) |

## サイトを手元で作る

```
node build.js
```

`site/` に HTML が出ます。Node.js 以外に必要なものはありません。

## ライセンス

© 2026 根本卓哉（Takuya Nemoto）— 本文・要旨ともに [CC BY 4.0](LICENSE)。出典を示せば、改変も含めて自由に使えます。
引用の書き方は [docs/how-to-cite.md](docs/how-to-cite.md) にあります。

## 執筆における AI の利用

二篇とも、改訂にあたって Claude（Anthropic）の助力を得ています。どの作業に使い、
どこまでを著者が引き受けているかは、各論文の末尾の開示文と
[docs/ai-disclosure.md](docs/ai-disclosure.md) に記載しています。

## 著者

根本卓哉（Takuya Nemoto）— 独立研究者
[プロフィール](https://cpsbvbng26-dotcom.github.io/cpsbvbng26-dotcom/) ｜
[ORCID](https://orcid.org/0009-0000-1406-0547)
