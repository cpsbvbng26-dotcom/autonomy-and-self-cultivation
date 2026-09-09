#!/usr/bin/env python3
"""references.toml から SHELF.md（書棚）を組み立てる。

    python3 verification/build_shelf.py

**この頁に、本の中身の要約は一行も無い。**大半を読んでいないからである。
書いてあるのは紙面から取れることだけ —— 書誌、どの論文が挙げているか、
論文自身の記述から立つ反論、そして**読んだら何が確かめられるか**。

最後の一つは本についての主張ではなく、**作業についての予定**である。
だから、読む前に書ける。
"""

import io
import os
import sys
import tomllib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

with io.open(os.path.join(HERE, "references.toml"), "rb") as fh:
    spec = tomllib.load(fh)

refs = spec["reference"]
paper = spec["paper"]
LABEL = {"F": "断章論", "M": "Manifesto", "N": "独身論"}


# 二段階に分ける。check_references.py と同じ切り方である。
#
#   意図   supports と role。**紙面と突き合わせられる。**本は要らない
#   確認   locus と agreement。**本が要る**
#
# 混ぜると、使い方は書けているのに「示せていない」と印字することになる。


def intended(r):
    return bool(str(r.get("supports", "")).strip()
                and str(r.get("role", "")).strip())


def verified(r):
    return bool(str(r.get("locus", "")).strip()
                and str(r.get("agreement", "")).strip())


def filled(r):
    return intended(r) and verified(r)


done = [r for r in refs if filled(r)]
todo = [r for r in refs if not filled(r)]
意図のみ = [r for r in refs if intended(r) and not verified(r)]
白紙 = [r for r in refs if not intended(r)]
指せない = set(spec.get("read_no_locus", []))
借り物 = [r for r in refs
          if str(r.get("origin", "")).strip() == "外から"
          and not str(r.get("agreement", "")).strip()]

out = []
w = out.append

w("# 書棚 —— まだ確かめていない %d 冊" % len(todo))
w("")
w("このファイルは `verification/references.toml` からの生成物である。"
  "手で編集しない。")
w("（`python3 verification/build_shelf.py` で作り直す）")
w("")
w("三篇の参考文献欄に載っている典拠を、一冊ずつ並べたものである。")
w("著者はこれらの原典の大半に当たっていない（[ERRATA.md](ERRATA.md) の `E6`）。")
w("")
w("> この頁に、本の中身の要約は一行もない。大半を読んでいないからである。")
w("> 書いてあるのは紙面から取れることだけ ―― 書誌、どの論文が挙げているか、")
w("> 論文自身の記述から立つ反論、読んだら何が確かめられるか。")
w("> 最後の一つは本についての主張ではない。作業についての予定である。")
w("")
w("欄は二段に分かれている。**本が要るのは下の段だけである。**")
w("")
w("| 段 | 欄 | 要るもの |")
w("| --- | --- | --- |")
w("| 意図 | `supports`（何を支えているか）・`role`（使い方） | 紙面だけ |")
w("| 確認 | `locus`（どの箇所か）・`agreement`（一致するか） | その本 |")
w("")
w("上の段は論文の紙面から書ける。下の段は本を開かないと書けない。")
w("埋めた日は git が持つ。")
w("")
w("| | |")
w("| --- | --- |")
w("| 合計 | %d 冊 |" % len(refs))
w("| 読んで、箇所も書いた | %d 冊 |" % len(done))
w("| 使い方は書いた、箇所は書けていない | %d 冊 |" % len(意図のみ))
w("| 何も書いていない | %d 冊 |" % len(白紙))
w("| まだ確かめていない | **%d 冊** |" % len(todo))
w("")
w("`origin` の欄がある本は、着想がどちら側から来たかを記している。")
w("`自前` は論文の着想が先にあった場合、`外から` は典拠が着想を供給した場合である。")
w("**外から来て、なお読んでいないものが %d 冊ある。**" % len(借り物))
w("そこでは主張そのものが人伝えの要約に乗っている。")
w("")
w("読んでいながら位置を指せないものが %d 冊ある。" % len(指せない))
w("**読んだことと、指せることは別である。**指せないものは未検証のまま置いてある。")
w("")
w("---")
w("")

for pid in ("F", "M", "N"):
    rows = [r for r in refs if r["paper"] == pid]
    if not rows:
        continue
    w("## %s（%d 冊）" % (LABEL[pid], len(rows)))
    w("")
    w("*%s*" % paper[pid])
    w("")
    for r in rows:
        mark = ("記入済み" if filled(r)
                else "読んだが、位置を指せない" if r["id"] in 指せない
                else "使い方は書いた・未確認" if intended(r)
                else "未記入")
        w("### %s" % r["bib"])
        w("")
        w("`%s` ｜ **%s**" % (r["id"], mark))
        w("")
        if r.get("note"):
            w("この一冊が特に効く理由。%s" % r["note"])
            w("")
        if intended(r):
            rows = []
            if verified(r):
                rows.append(("箇所", r["locus"]))
            rows.append(("支えているもの", r["supports"]))
            rows.append(("使い方", r["role"]))
            if verified(r):
                rows.append(("典拠との一致", r["agreement"]))
            if r.get("origin"):
                rows.append(("着想の出どころ", r["origin"]))
            if r.get("caveat"):
                rows.append(("留保", r["caveat"]))
            w("| %s | %s |" % rows[0])
            w("| --- | --- |")
            for k, v in rows[1:]:
                w("| %s | %s |" % (k, v))
            if not verified(r):
                w("")
                if r["id"] in 指せない:
                    w("想定される反論。著者はこの本を読んでいると述べている。"
                      "ただし、どの箇所がこの主張を支えているかは書けていない。"
                      "読んだことと、指せることは別である。")
                    w("")
                    w("読んだら確かめられること。この本のどの巻が、"
                      "ここに書いた使い方を支えているか。その本を持つ者なら、"
                      "著者より先に書ける。")
                    w("")
                    continue
                w("想定される反論。使い方は書けているが、"
                  "この本のどの箇所がそれを支えているかは書けていない。")
                w("")
                if str(r.get("origin", "")).strip() == "外から":
                    w("読んだら確かめられること。ここに書いた使い方が、"
                      "実際にこの本の述べていることか。"
                      "**着想がこの本から来ているので、外れれば主張が残らない。**")
                else:
                    w("読んだら確かめられること。ここに書いた使い方が、"
                      "実際にこの本の述べていることか。外れていれば、そう書ける。")
        else:
            w("想定される反論。この典拠が論文のどの主張を支えているのか、"
              "著者は示せていない。")
            w("")
            w("読んだら確かめられること。この本のどの箇所が、論文のどの主張を"
              "支えているか。支えていないなら、そう書ける。")
        w("")
    w("---")
    w("")

w("## 反論に備えるとはどういうことか")
w("")
w("「読んだ」は備えではない。証言であり、外からは確かめられない。")
w("")
w("備えとは、「この箇所が、この主張を支えている」と書くことである。")
w("それは公開された主張であり、その本を持つ者なら誰でも覆せる。")
w("")
w("覆せる形にすることが備えである。")
w("")
w("使い方だけを書いた %d 冊は、そこまでは備えている。" % len(意図のみ))
w("紙面から読み取れることは書いた。その先は本を開かないと書けない。")
w("何も書いていない %d 冊は、そこまでも備えていない。" % len(白紙))

path = os.path.join(ROOT, "SHELF.md")
io.open(path, "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n")
print("書きました: SHELF.md（%d 冊、うち未読 %d 冊）" % (len(refs), len(todo)))
