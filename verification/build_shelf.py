#!/usr/bin/env python3
"""references.toml から SHELF.md（書棚）を組み立てる。

    python3 verification/build_shelf.py

**この頁に、本の中身の要約は一行も無い。**読んでいないからである。
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


def filled(r):
    return bool(str(r.get("locus", "")).strip()
                and str(r.get("supports", "")).strip()
                and str(r.get("role", "")).strip())


done = [r for r in refs if filled(r)]
todo = [r for r in refs if not filled(r)]

out = []
w = out.append

w("# 書棚 —— まだ読んでいない %d 冊" % len(todo))
w("")
w("**このファイルは `verification/references.toml` から生成しています。"
  "手で編集しないでください。**")
w("（`python3 verification/build_shelf.py` で作り直します）")
w("")
w("三篇の参考文献欄に載っている典拠を、一冊ずつ並べたものです。")
w("**著者はこれらの原典に当たっていません**（[ERRATA.md](ERRATA.md) の `E6`）。")
w("")
w("> **この頁に、本の中身の要約は一行もありません。**読んでいないからです。")
w("> 書いてあるのは紙面から取れることだけ —— 書誌、どの論文が挙げているか、")
w("> **論文自身の記述から立つ反論**、そして**読んだら何が確かめられるか**。")
w("> 最後の一つは本についての主張ではなく、**作業についての予定**です。")
w("")
w("読んだ本から、`references.toml` の `locus`（どの箇所か）・"
  "`supports`（何を支えているか）・`role`（使い方）が埋まります。")
w("**埋めた日は git が持ちます。**")
w("")
w("| | |")
w("| --- | --- |")
w("| 合計 | **%d 冊** |" % len(refs))
w("| 読んで記入済み | **%d 冊** |" % len(done))
w("| **まだ読んでいない** | **%d 冊** |" % len(todo))
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
        mark = "記入済み" if filled(r) else "未読"
        w("### %s" % r["bib"])
        w("")
        w("`%s` ｜ **%s**" % (r["id"], mark))
        w("")
        if r.get("note"):
            w("**この一冊が特に効く理由。** %s" % r["note"])
            w("")
        if filled(r):
            w("| 箇所 | %s |" % r["locus"])
            w("| --- | --- |")
            w("| 支えているもの | %s |" % r["supports"])
            w("| 使い方 | %s |" % r["role"])
            if r.get("caveat"):
                w("| 留保 | %s |" % r["caveat"])
        else:
            w("**想定される反論。**「この典拠が、論文のどの主張を支えているのか、"
              "著者は示せていない」")
            w("")
            w("**読んだら確かめられること。**この本のどの箇所が、"
              "論文のどの主張を支えているのか。支えていないなら、そう書けます。")
        w("")
    w("---")
    w("")

w("## 反論に備えるとはどういうことか")
w("")
w("**「読みました」と言うことではありません。**それは証言であって、")
w("外から確かめられません。")
w("")
w("**「この箇所が、この主張を支えている」と書くこと**です。それは公開された")
w("主張であり、**その本を持っている人なら誰でも覆せます。**")
w("")
w("覆せる形にすることが、備えです。**いまは %d 冊ぶん、備えがありません。**"
  % len(todo))

path = os.path.join(ROOT, "SHELF.md")
io.open(path, "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n")
print("書きました: SHELF.md（%d 冊、うち未読 %d 冊）" % (len(refs), len(todo)))
