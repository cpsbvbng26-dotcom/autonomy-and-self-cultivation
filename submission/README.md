# 投稿用の原稿

Conatus – Journal of Philosophy に出す一篇の、投稿用のファイルです。

| | |
| --- | --- |
| 対象 | The Nobility and Exemplarity of the Celibate Individual |
| 公開版 | [`10.5281/zenodo.22058254`](https://doi.org/10.5281/zenodo.22058254)（v2、2026年8月22日） |
| 体裁 | Times New Roman 12pt、行間シングル、両端揃え。誌の投稿規程に合わせた |

**凍結された PDF には触っていない**（決めごと 2）。これは別のファイルです。

## 本文は変えていない

落としたものは三つだけです。

1. 扉の著者行 —— 匿名の査読に回るため
2. 扉の書誌の表 —— DOI・ライセンス・PDF への参照
3. 日本語による要旨 —— 誌の言語は英語です

**AI 支援の開示は落としていない**（決めごと 8）。著者を指さないので、匿名の査読でも残せます。

一字も変えていないことは機械で確かめます。

```
python3 verification/check_manuscript.py
```

公開されている本文から同じ手順で文字だけを取り出し、原稿から取り出したものと
突き合わせます。一字でも違えば落ちます。壊して確かめてあります。

## 作り直し方

```
cd submission && npm install docx && node build.js
```

`manuscript.md` が原稿の元です。`papers/celibate-individual.md` から
上の三つを落として作りました。手で編集しません。

## この環境で確かめられないこと

紙面の見た目は確かめていません。LibreOffice がこの作業環境で壊れており、
最小の docx すら開けません。体裁が規程どおりに出ているかは、そちらの画面で見ること。
