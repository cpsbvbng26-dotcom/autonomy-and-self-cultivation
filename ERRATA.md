# 正誤表 —— 哲学の三篇

最終更新: 2026年9月8日

三篇の PDF は Zenodo・SSRN・PhilArchive で公開済みで、**もう直せません。**
直せるのはこの文書のほうです。だからこの文書のほうが、時間とともに紙面から
ずれていきます。**そのずれは検査で落とします**（`verification/check_errata.py`）。

対象は次の三篇です。SHA-256 を宣言してあるので、**紙面そのものが差し替われば
検査が落ちます。**

| 略号 | 題 |
| --- | --- |
| **N** | The Nobility and Exemplarity of the Celibate Individual（v2） |
| **M** | Manifesto of Imperial Selfhood（Revised and Expanded Edition） |
| **F** | Fragmentarian Spiritual Individualism |

---

## E1 — 三篇とも、自身の DOI を印字していない

**重大度: 中（PDF だけを手にした読者が、正本に辿り着けない）**

三篇とも Zenodo に登録され DOI が付与されていますが、**紙面のどこにも印字されて
いません。**

| | DOI | 紙面に印字 |
| --- | --- | --- |
| N | [10.5281/zenodo.22058254](https://doi.org/10.5281/zenodo.22058254) | 無し |
| M | [10.5281/zenodo.22057583](https://doi.org/10.5281/zenodo.22057583) | 無し |
| F | [10.5281/zenodo.22064241](https://doi.org/10.5281/zenodo.22064241) | 無し |

PDF が単体で出回ると、読者は正本にも改訂版にも辿り着けません。表紙に一行あれば
済んだことです。

**この項目は解決しません。**紙面は直せないので、ここに DOI を置いて残します。

## E2 — 三篇とも、ORCID を印字していない

**重大度: 低**

著者の ORCID は [0009-0000-1406-0547](https://orcid.org/0009-0000-1406-0547) ですが、
**三篇のどこにも印字されていません。**同姓同名との区別が紙面だけではつきません。

**この項目は解決しません。**

## E3 — N は初版を指しているが、初版の DOI を示していない

**重大度: 中**

N の表紙にはこう印字されています。

> Original version: 21 October 2025 | Revised version (v2): 22 August 2026

**初版がどこにあるかは書かれていません。** DOI も URL もありません。読者は
「改訂された」と知らされたうえで、**何が改訂されたのかを確かめる手段を持ちません。**

改訂で何が変わったかの記録は、このリポジトリの側にあります。

**この項目は解決しません。**

## E4 — M の表紙が挙げる頒布先のうち、一つが現在は無い

**重大度: 中**

M の表紙にはこう印字されています。

> Prepared for open-access distribution via Zenodo, Academia.edu, and ResearchGate.

2026年9月8日に著者が確認した所在は次のとおりです。

| 所在 | 確認 |
| --- | --- |
| Zenodo [10.5281/zenodo.22057583](https://doi.org/10.5281/zenodo.22057583) | あり |
| SSRN [10.2139/ssrn.7358818](https://doi.org/10.2139/ssrn.7358818) | あり |
| PhilArchive [NEMMOI](https://philarchive.org/rec/NEMMOI) | あり |
| [Academia.edu](https://independent.academia.edu/NemotoTakuya) | あり |
| ResearchGate | 著者が置いたものは**無い**。索引が自動生成した頁がある（下記） |

**紙面が誤っていたのではありません。**ResearchGate の頁は著者が削除しました。
そのあと、SSRN 版から索引が拾い直しています。

### ResearchGate 側の状態（2026年9月8日）

著者が置き直したのではなく、**ResearchGate が SSRN の記録から自動生成**した
「scientific contributions」の頁です。しかも**同一人物が二つに分かれています。**

| 頁 | 由来 |
| --- | --- |
| [Takuya-Nemoto-2367530856](https://www.researchgate.net/scientific-contributions/Takuya-Nemoto-2367530856) | SSRN の二篇のうち一方 |
| [Takuya-Nemoto-2367530944](https://www.researchgate.net/scientific-contributions/Takuya-Nemoto-2367530944) | もう一方 |

SSRN にあるのは
[10.2139/ssrn.7358779](https://doi.org/10.2139/ssrn.7358779)（独身論）と
[10.2139/ssrn.7358818](https://doi.org/10.2139/ssrn.7358818)（M）の二篇で、
**論文ごとに別人として登録されています。**索引の側の名寄せの失敗であって、
著者の側で直せるものではありません。この二つが同一人物であることは、
プロフィールの `sameAs` に両方を並べる形で機械可読にしてあります。

### それでも解決しない理由

紙面は「頒布する」と述べています。いまそこにあるのは**索引が勝手に作った記録**で、
著者が置いた頒布物ではありません。加えて、この状態は向こうの都合でいつでも
変わります —— 二つが統合されるかもしれないし、消えるかもしれない。

E1・E2・E3 は紙面の側の誤りでしたが、この項目はそうではなく、**紙面が正しかった
まま合わなくなり、また合いかけている**例です。凍結された紙面は、行ったり来たり
する事実に追随できません。どちらも紙面を直せない点では同じです。

**この項目は解決しません。**

---

## 正誤ではないが、記録しておくこと

### N1 — 本文の引用と参考文献欄は、三篇とも食い違っていない

`(著者 年)` の形で本文に現れる引用を機械で拾い、参考文献欄に対応する項目が
あるかを突き合わせました。**三篇とも食い違いはありませんでした。**

これは「調べたが何も出なかった」という記録です。**調べていないことと、調べて
何も出なかったことは違います。**

### N2 — その照合が、一度だけ偽陽性を出した

最初の実装では、M の本文にある `(Nietzsche 1967)` を「参考文献欄に無い」と
報告しました。**照合の窓が狭かっただけで、実際には**

> Nietzsche, Friedrich. The Will to Power. Translated by Walter Kaufmann and R. J. Hollingdale. New York: Vintage, 1967.

が参考文献欄にあります。同じ著者の項目が三つ並んでおり、1967 の項目が三つ目
だったため、窓の外に出ていました。

**検査の側の誤りです。**紙面は正しく、こちらが間違えました。窓を広げて解消して
います。記録として残します。

### N3 — 三篇とも、査読前であることを明示している

三篇とも「Preprint. This work has not been peer reviewed.」ないし同等の記述を
表紙に持っています。**これは守られています。**

### N4 — 三篇とも、AI の使用を開示している

三篇とも、AI（Claude）を草稿・構成・推敲に用いたことと、著者が内容に責任を負う
ことを明記しています。**AI を著者として挙げてはいません。**

---

## 見つけ方

E1・E2・E3・E4 は、PDF から文字を取り出して機械で拾いました。N1・N2 は本文と
参考文献欄の突き合わせの副産物です。

**この文書が「印字されている」と述べていることは、
[`verification/check_errata.py`](verification/check_errata.py) が PDF から文字を
取り出して突き合わせています。**引用が一字でも合わなくなれば、そこで落ちます。

道具は [errata-check](https://github.com/cpsbvbng26-dotcom/errata-check)
（MIT、v0.2.0、[10.5281/zenodo.22649899](https://doi.org/10.5281/zenodo.22649899)）です。
単一ファイルなので写して使っています。

**この文書自体は査読ではありません。**見つかったものを記録しただけです。
