# 自律と自己陶冶

**自分の生をどこまで自分で治められるか**を主題にした、三篇のプレプリントを収めたリポジトリです。

一篇は独身（celibacy）を、性的活動の欠落ではなく擁護しうる自己陶冶の型として読み直します。
一篇は、断片化した自己を統合する試みを「人格的帝国主義」という概念のもとで素描します。
残る一篇は逆に、断片化を修復すべき傷ではなく生の実際の姿として受け取り、そこに住まうための規律を組み立てます。

主題は離れて見えますが、問いは共通しています —— **何を基準に、自分の生の形を決めるのか**。
統合を目指す二篇目と、統合を諦める三篇目が並んでいるのは、矛盾ではなく問いの幅です。

どちらも査読前の原稿です。著者による公開は SSRN・PhilArchive などの窓口で行っており、
このリポジトリは**全文を読める形に開き、版と出典をひとところに置くため**のものです。

## 三篇

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

### [Fragmentarian Spiritual Individualism](papers/fragmentarian-spiritual-individualism.md)

*A Philosophy of Fragments for Solitary Spiritual Autonomy* — 2026年8月

生・信仰・社会・思想・終末を、ひとつづきの物語ではなく独立した断片として扱います。断片化を修復すべき傷と
みなす通例に対し、それが生の実際のあり方の記述として正確なのではないかと問い、克服ではなく
**厳密さをもって住まう**ための規律を組み立てます。実存主義・キリスト教神秘主義・武士道・戦後日本の
批評（吉本隆明、柄谷行人）からの総合です。

[全文](papers/fragmentarian-spiritual-individualism.md) ｜ [PDF](pdf/fragmentarian-spiritual-individualism.pdf)

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

本文は PDF から起こしたもので、書き写したものではありません。抽出した語の並びと照合しています。

| | 語数 | 一致 | 差 |
| --- | --- | --- | --- |
| 独身論 | 3739 | 3739 | なし |
| 人格的帝国主義 | 4368 | 4364 | ハイフン語の結合 4 |
| 断片主義 | 5173 | 5165 | ハイフン語の結合 4、抽出器が入れた余分な空白 4 |

`non-negotiable` `self-overcoming` のように**行末で割れた語を繋ぎ直した**もの、および
`( Seelengrund)` のように**抽出器が括弧の内側に入れてしまった空白を取り除いた**ものだけで、
それ以外に手を入れた箇所はありません。

日本語の要旨だけは、このリポジトリのために書き下ろしたもので、原文にはありません。

## 公開先

著者ページと、各論文の識別子です。

**はじめの二篇は Zenodo と SSRN の両方に登録されており、DOI が 2 つあります。**
引用の際は Zenodo の DOI を用いてください（こちらを正とします）。SSRN の DOI は同一の本文を指します。

| | |
| --- | --- |
| SSRN | [著者ページ](https://papers.ssrn.com/sol3/cf_dev/AbsByAuth.cfm?per_id=8730280) |
| 独身論 | [10.5281/zenodo.22058254](https://doi.org/10.5281/zenodo.22058254)（SSRN: [10.2139/ssrn.7358779](https://doi.org/10.2139/ssrn.7358779)） |
| 人格的帝国主義 | [10.5281/zenodo.22057583](https://doi.org/10.5281/zenodo.22057583)（SSRN: [10.2139/ssrn.7358818](https://doi.org/10.2139/ssrn.7358818)） |
| 断片主義 | [10.5281/zenodo.22064241](https://doi.org/10.5281/zenodo.22064241) |
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

[![Built with Claude Code](https://img.shields.io/badge/Built%20with-Claude%20Code-D97757?style=for-the-badge&logo=claude&logoColor=white)](https://claude.com/claude-code)
[![Assisted by Grok](https://img.shields.io/badge/Assisted%20by-Grok-111111?style=for-the-badge)](https://grok.com)

三篇とも、執筆または改訂にあたって Claude（Anthropic）の助力を得ています。どの作業に使い、
どこまでを著者が引き受けているかは、各論文の末尾の開示文と
[docs/ai-disclosure.md](docs/ai-disclosure.md) に記載しています。

## 著者

根本卓哉（Takuya Nemoto）— 独立研究者
[プロフィール](https://cpsbvbng26-dotcom.github.io/cpsbvbng26-dotcom/) ｜
[ORCID](https://orcid.org/0009-0000-1406-0547)
