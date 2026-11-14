# 手を入れるときに

Issue も pull request も歓迎する。登録は要らない。

## ここに何があるか

凍結された哲学の論文と、その正誤表と、両者を突き合わせる検査である。
[SHELF.md](SHELF.md) が棚の状態を、[ERRATA.md](ERRATA.md) が誤りを持っている。

## いちばん知らせてほしいもの

紙面の誤りである。とくに次の二つ。

1. 典拠の誤り。引いた哲学者が、実際にはそう述べていない場合。
   **原典の頁を添えてほしい**
2. 論証の穴。前提から結論が出ていない場合。どの段が飛んでいるか

<https://github.com/cpsbvbng26-dotcom/autonomy-and-self-cultivation/issues> に立てる。

正誤表に E6 として書いてあるとおり、典拠の一部は著者が原典に当たっていない。
重大度は高い。そこを突く指摘は、いちばん価値がある。

## PDF を直さない

公開済みの PDF は改変も再生成もしない。凍結された成果物である。
誤りが見つかったら、直すのは PDF ではなく正誤表のほうである。

`verification/check_errata.py` が、正誤表の各項目と紙面の実際の文字列を突き合わせている。
紙面を書き換えれば、正誤表のほうが嘘になる。

## 変更を出す

```
node build.js
pip install pypdf==6.19.0
python3 verification/check_fidelity.py -v   # 紙面との一致
python3 verification/check_errata.py        # 正誤表の監査
python3 verification/check_references.py    # 参考文献
node verification/check_text.js             # 誤変換とバッジ記法
```

通ってから出す。

## 立場を裁定しない

この棚は、どの哲学的立場が正しいかを決めない。論文が主張していることと、
その根拠と、確かめられていない部分を分けて書く。

「著者に賛成できない」という指摘は、それ自体では受けられない。
受けられるのは、**論証の形か、典拠の事実**についての指摘である。

## 通らない変更

- **検査の期待値を、通すために変えること**
- **PDF の改変・再生成**
- 正誤表の項目を消すこと。直した項目も、直したと書いて残す
- **推測で埋めた DOI**

## 支えの範囲と、これからの見込み

- **維持しているのは著者一人である**（根本卓哉）。組織の後ろ盾は無い
- issue への返答は**数日から一週間**を目安とする。約束ではない
- 範囲。この棚に載っている論文と、その正誤表に限る
- 査読を受けていない。プレプリントである。格上げして引かないこと

## 画像の代替テキスト

サイトの頁に画像を置くときは、`alt` に、その画像が伝えている中身を書く。
「画像」「写真」「図」や image で始めない。ファイル名を書かない。
飾りだけの画像は `alt=""` にして、読み上げから外す。
文字を画像にしない。文字は文字で書く。
`verification/check_site.js` が、`alt` の無い画像と、決めに沿わない書き方を落とす。

## ライセンス

散文と論文は [CC BY 4.0](LICENSE)、実装は [MIT](LICENSE-CODE)。

## 突き合わせの受付 / Checked intake

2026-12-01 から、誤りの知らせ（`error-report.yml`）は「突き合わせの受付」で確かめる。
人が嘘をつくこと一般は、仕組みでは止められない。受けるのは、申し立てた人がその場で書けない出どころと突き合わせられる申し立てだけで、通らないものと確かめられないものは自動で退ける。
確かめるのは一つだけである。「書いてあること」の語が、「どこか」の欄に書いた所（このリポジトリのファイル、配っている頁、このリポジトリが写しを持つ DOI の PDF か翻刻）に、そのとおりにあること。空白の違いと文字の幅は見ない。頁や節は確かめず、文書の全体を探す。
あればラベル「quote verified」を付ける。それが誤りかどうかは、人が読んで決める。なければ、決まった文のコメントを付けて閉じる。新しい issue で出し直せる。
削除・権利・個人の情報・氏名・人についての記述・同意の撤回を求めると読める issue は、自動では閉じない。ラベル「needs a person」を付け、人が読む。
コメントと実行の記録は、決まった語と issue の番号だけを書き、issue に書かれたことを写さない。
道具は `.github/checked-intake/verify.js`、確かめる先は `.github/checked-intake/config.json` にある。

From 2026-12-01, error reports (`error-report.yml`) are checked by the checked intake.
No system can stop a person from lying in general. Only claims that can be checked against a source that the claimant does not write at the moment of claiming are accepted; a claim that fails, or cannot be checked, is turned away automatically.
One thing is checked: that the words under "What it says" occur, as written, at the location under "Where" (a file of this repository, a page that it serves, or the PDF or transcription of a DOI of which it holds a copy). Differences of white space and character width are ignored. The page or section is not checked; the whole document is searched.
If they occur, the label "quote verified" is added, and whether it is an error is decided by a person. If they do not, the issue is closed with a fixed comment, and a new issue can be opened.
An issue that reads as asking for removal, or concerning rights, personal data, a name, a statement about a person or the withdrawal of a consent, is never closed automatically; it gets the label "needs a person", and a person reads it.
Comments and logs carry only fixed words and the issue number, never what the issue says.
The script is `.github/checked-intake/verify.js`; what it checks against is in `.github/checked-intake/config.json`.
