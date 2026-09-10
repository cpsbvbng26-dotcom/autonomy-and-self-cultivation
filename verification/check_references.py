#!/usr/bin/env python3
"""参考文献の宣言が、紙面と食い違っていないかを見る。

    python3 verification/check_references.py

**この検査は「読んだか」を見ない。**内面は外から確かめられない。見るのは
宣言と紙面の整合だけである。

**空欄であることは失敗ではない。**確認の段は空欄が既定である（ERRATA の `E6`）。
失敗になるのは、

  - 宣言した典拠が、その論文の紙面に無いとき（でっち上げ）
  - 埋めた項目が、決まりを満たしていないとき
  - 読んだ箇所を書かずに、一致だけを主張したとき
  - 位置を指せないと宣言した項目に、位置が書かれたとき
  - **件数を、散文が実際と違う数で名乗っているとき**

の五つである。**何件が埋まっているかを、機械が数えて散文と突き合わせる。**
埋めた日は git が持つので、あとから遡って埋めたことにはできない。
"""

import io
import os
import re
import sys
import tomllib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from errata_check import extract_text, normalize   # noqa: E402

ROLES = ("直接支持", "用語の出所", "対立見解", "背景", "反例")

PDF = {
    "F": "pdf/fragmentarian-spiritual-individualism.pdf",
    "M": "pdf/manifesto-of-imperial-selfhood-revised.pdf",
    "N": "pdf/nobility-and-exemplarity-of-the-celibate-individual-v2.pdf",
}

passed, failures = 0, []


def check(label, ok, detail=""):
    global passed
    if ok:
        passed += 1
        print("  PASS  " + label + (("  " + detail) if detail else ""))
    else:
        failures.append(label)
        print("  FAIL  " + label + (("  " + detail) if detail else ""))


with io.open(os.path.join(HERE, "references.toml"), "rb") as fh:
    spec = tomllib.load(fh)
refs = spec.get("reference", [])

print("\n1. 宣言の形")

ids = [r.get("id", "") for r in refs]
check("id が重複していない", len(set(ids)) == len(ids), "%d 件" % len(ids))
check("すべてに論文の別がある",
      all(r.get("paper") in PDF for r in refs),
      "、".join(sorted(set(str(r.get("paper")) for r in refs))))
check("すべてに bib がある", all(str(r.get("bib", "")).strip() for r in refs))

print("\n2. 宣言した典拠が、その論文の紙面にあるか")

text = {}
for pid, path in PDF.items():
    text[pid] = normalize(extract_text(os.path.join(ROOT, path)))

missing = [r["id"] for r in refs
           if normalize(r["bib"]) not in text.get(r.get("paper"), "")]
check("宣言した典拠がすべて紙面にある", not missing,
      ("紙面に無い: " + "、".join(missing[:5])) if missing
      else "%d 件を三篇の参考文献欄と突き合わせた" % len(refs))

print("\n3. 埋めた項目が、決まりを満たしているか")


# 二段階に分ける。**混ぜると、意図が分かっているのに書けない状態が続く。**
#
#   意図   supports と role。**紙面と突き合わせられる。**本は要らない
#   確認   locus と agreement。**本が要る**
#
# 意図だけ埋めることは認める。確認だけ埋めることは認めない ——
# どこを読んだかを書かずに一致を主張することはできない。

def intended(r):
    """意図が書かれているか。supports と role。"""
    return bool(str(r.get("supports", "")).strip()
                and str(r.get("role", "")).strip())


def verified(r):
    """典拠を確認したか。locus と agreement。"""
    return bool(str(r.get("locus", "")).strip()
                and str(r.get("agreement", "")).strip())


def filled(r):
    return intended(r) and verified(r)


done = [r for r in refs if filled(r)]
todo = [r for r in refs if not filled(r)]

# 一つの典拠が二つの役を兼ねることはある。用語の出所であり、同時に直接支持でも
# あるという場合である。だから `role` は「・」で区切って並べられる。
# **並べられるのは決めた五つだけで、同じ語を二度は書けない。**


def roles(r):
    return [x for x in str(r.get("role", "")).split("・") if x.strip()]


bad_role = [r["id"] for r in refs
            if str(r.get("role", "")).strip()
            and any(x not in ROLES for x in roles(r))]
check("使い方が決めた語である", not bad_role,
      "、".join(bad_role) or "使えるのは " + "・".join(ROLES) + "（「・」で兼ねられる）")

dup_role = [r["id"] for r in refs if len(roles(r)) != len(set(roles(r)))]
check("同じ使い方を二度書いた項目が無い", not dup_role, "、".join(dup_role))

兼 = [r["id"] for r in refs if len(roles(r)) > 1]
check("役を兼ねる項目を数えている", True,
      "%d 件（%s）" % (len(兼), "、".join(兼)) if 兼 else "無い")

half_i = [r["id"] for r in refs
          if not intended(r) and any(str(r.get(k, "")).strip()
                                     for k in ("supports", "role"))]
check("意図が途中まででない", not half_i,
      ("supports と role は揃えて埋める: " + "、".join(half_i[:5])) if half_i else "")

half_v = [r["id"] for r in refs
          if not verified(r) and any(str(r.get(k, "")).strip()
                                     for k in ("locus", "agreement"))]
check("確認が途中まででない", not half_v,
      ("locus と agreement は揃えて埋める: " + "、".join(half_v[:5])) if half_v else "")

no_intent = [r["id"] for r in refs if verified(r) and not intended(r)]
check("確認だけが書かれた項目が無い", not no_intent,
      ("何を支える引用なのかを書かずに確認だけを書けない: " + "、".join(no_intent[:5]))
      if no_intent else "")

check("意図と確認を分けて数えている", True,
      "意図 %d / 39・確認 %d / 39" % (sum(1 for r in refs if intended(r)),
                                      sum(1 for r in refs if verified(r))))

# 「原典に当たっていない」は手続きの記述であって、引用が誤っていることを意味しない。
# 一致・部分一致・不一致・未検証を分けて数える。**空欄は未検証である。**
# 一致だった場合、それは Trinity-Infinity 側で「再発見」と呼んだ形と同じである。
AGREEMENT = ("一致", "部分一致", "不一致")

bad_agree = [r["id"] for r in refs
             if str(r.get("agreement", "")).strip()
             and str(r.get("agreement", "")).strip() not in AGREEMENT]
check("agreement が決めた語である", not bad_agree,
      "、".join(bad_agree) or "使えるのは " + "・".join(AGREEMENT) + "（空欄は未検証）")

no_agree = [r["id"] for r in done if not str(r.get("agreement", "")).strip()]
check("埋めた項目には agreement がある", not no_agree,
      ("典拠を読んだのなら一致か否かを書く: " + "、".join(no_agree[:5])) if no_agree else "")

早い = [r["id"] for r in refs
        if str(r.get("agreement", "")).strip()
        and not str(r.get("locus", "")).strip()]
check("読まずに一致だけを書いた項目が無い", not 早い,
      ("locus の無い agreement は根拠が無い: " + "、".join(早い[:5])) if 早い else "")

tally = {k: sum(1 for r in refs if str(r.get("agreement", "")).strip() == k)
         for k in AGREEMENT}
未検証 = sum(1 for r in refs if not str(r.get("agreement", "")).strip())
check("引用の一致を数えている", True,
      "一致 %d / 部分一致 %d / 不一致 %d / 未検証 %d"
      % (tally["一致"], tally["部分一致"], tally["不一致"], 未検証))

# 未読であることの重さは、典拠ごとに違う。着想が先にあった場合と、典拠が着想を
# 供給した場合を分けて数える。**外から来ていて、なお読んでいないものが、いちばん深い。**
# この差は利用者の証言であって、紙面からは出ない。だから紙面との突き合わせは掛からない。
ORIGINS = ("自前", "外から")

bad_origin = [r["id"] for r in refs
              if str(r.get("origin", "")).strip()
              and str(r.get("origin", "")).strip() not in ORIGINS]
check("origin が決めた語である", not bad_origin,
      "、".join(bad_origin) or "使えるのは " + "・".join(ORIGINS) + "（空欄は未記載）")

# origin は本文で使われている典拠についてしか言えない。使われていないものに
# 「着想が先にあった」も「着想を供給した」も無い。
no_body_origin = [r["id"] for r in refs
                  if r["id"] in set(spec.get("body_absent", []))
                  and str(r.get("origin", "")).strip()]
check("本文に無い項目に origin が書かれていない", not no_body_origin,
      ("引かれていないのに origin がある: " + "、".join(no_body_origin))
      if no_body_origin else "")

# origin を書くには、その典拠が何を支えているかが先に要る。
# **着想の出どころだけ書いて、使い方を書かないことは認めない。**
origin_no_intent = [r["id"] for r in refs
                    if str(r.get("origin", "")).strip() and not intended(r)]
check("origin だけが書かれた項目が無い", not origin_no_intent,
      ("何を支える引用なのかを書かずに origin を書けない: "
       + "、".join(origin_no_intent[:5])) if origin_no_intent else "")

o_tally = {k: sum(1 for r in refs if str(r.get("origin", "")).strip() == k)
           for k in ORIGINS}
未記載 = sum(1 for r in refs if not str(r.get("origin", "")).strip())
check("着想の出どころを数えている", True,
      "自前 %d / 外から %d / 未記載 %d"
      % (o_tally["自前"], o_tally["外から"], 未記載))

# **いちばん深い組み合わせ。**着想が典拠から来ていて、その典拠を読んでいない。
# 主張そのものが人伝えの要約に乗っている。散文がこの数を名乗るなら、突き合わせる。
借り物 = [r["id"] for r in refs
          if str(r.get("origin", "")).strip() == "外から"
          and not str(r.get("agreement", "")).strip()]
check("外から来て、なお読んでいないものを数えている", True,
      "%d 件（%s）" % (len(借り物), "、".join(借り物)) if 借り物 else "無い")

# 参考文献欄にあるだけで、本文から引かれていない項目。
#
# **以前の検査は、参考文献の行に文字列があれば通していた。**本文で使われているかを
# 見ていなかった。実際に一件（Foucault）を見落としていた。
#
# 探索語は id の真ん中から取り、取れないものは body_key を書く。
# **Jünger を junger で探して誤検出した。**綴りは合わせる。

# 読んだと述べていながら、locus を書けない項目。
# **読んだことと、指せることは別である。**確認として数えるのは後者だけである。

print("\n3.4 読んだと述べていながら、位置を指せないもの")

指せない = spec.get("read_no_locus", [])
未知 = [i for i in 指せない if i not in set(ids)]
check("宣言した id が実在する", not 未知, "、".join(未知))
埋まった = [r["id"] for r in refs if r["id"] in set(指せない)
            and (str(r.get("locus", "")).strip()
                 or str(r.get("agreement", "")).strip())]
check("位置を指せないと宣言した項目に、locus も agreement も無い", not 埋まった,
      ("書けたのなら宣言から外す: " + "、".join(埋まった)) if 埋まった else "")
半端 = [r["id"] for r in refs if r["id"] in set(指せない) and not intended(r)]
check("位置を指せない項目にも、何を支えるかは書いてある", not 半端,
      "、".join(半端))
check("読んだと述べていながら位置を指せないものを数えている", True,
      "%d 件（%s）" % (len(指せない), "、".join(指せない)) if 指せない else "無い")

print("\n3.5 参考文献欄にあって本文に無いもの")

declared = set(spec.get("body_absent", []))
absent = []
for pid in PDF:
    whole = text[pid]
    i = whole.rfind("References")
    body = whole[:i] if i > 0 else whole
    for r in [x for x in refs if x["paper"] == pid]:
        key = r.get("body_key") or r["id"].split("-")[1]
        if key.lower() not in body.lower():
            absent.append(r["id"])
absent = sorted(set(absent))
check("本文に無い項目が、宣言したものと一致する", absent == sorted(declared),
      ("宣言 %s / 実際 %s" % (sorted(declared), absent)) if absent != sorted(declared)
      else ("%d 件（%s）" % (len(absent), "、".join(absent)) if absent else "無い"))
no_role = [r["id"] for r in refs if r["id"] in declared
           and (str(r.get("role", "")).strip() or str(r.get("supports", "")).strip())]
check("本文に無い項目に、支える主張が書かれていない", not no_role,
      ("引かれていないのに supports か role がある: " + "、".join(no_role)) if no_role else "")

print("\n3.6 本文が名を挙げていて、参考文献欄に無いもの")

# **向きが逆の抜け。**参考文献欄にある項目が本文で使われているかは 3.5 が見ている。
# 本文が名を挙げた相手が参考文献欄にあるかは、どこも見ていなかった。
only = []
for spec_line in spec.get("body_only", []):
    pid, _, key = str(spec_line).partition(":")
    whole = text.get(pid, "")
    i = whole.rfind("References")
    body, tail = (whole[:i], whole[i:]) if i > 0 else (whole, "")
    in_body = key.lower() in body.lower()
    in_refs = key.lower() in tail.lower()
    only.append((spec_line, in_body, in_refs))
    check("「%s」が本文にある" % spec_line, in_body)
    check("「%s」が参考文献欄に無い" % spec_line, not in_refs)
check("本文だけに出る名を数えている", True,
      "%d 件（%s）" % (len(only), "、".join(x[0] for x in only)) if only else "無い")

print("\n4. 散文が名乗る残り件数")

errata = io.open(os.path.join(ROOT, "ERRATA.md"), encoding="utf-8").read()
m = re.search(r"未記入は \*\*(\d+) 件\*\*", errata)
check("ERRATA.md が名乗る未記入の件数が実際と合う",
      m is not None and int(m.group(1)) == len(todo),
      ("名乗り %s / 実際 %d" % (m.group(1) if m else "無し", len(todo))))

# 二段の表。**上の段が埋まったことを、読んだことのように読ませない。**
for 段, 実際 in (("意図", sum(1 for r in refs if intended(r))),
                 ("確認", sum(1 for r in refs if verified(r)))):
    m5 = re.search(r"\| %s \|[^|]*\| \*\*(\d+) / %d\*\* \|" % (段, len(refs)), errata)
    check("ERRATA.md が名乗る「%s」の件数が実際と合う" % 段,
          m5 is not None and int(m5.group(1)) == 実際,
          "名乗り %s / 実際 %d" % (m5.group(1) if m5 else "無し", 実際))

m6 = re.search(r"読んでいながら位置を指せないものが \*\*(\d+) 件\*\*", errata)
check("ERRATA.md が名乗る、位置を指せないものの件数が実際と合う",
      m6 is not None and int(m6.group(1)) == len(指せない),
      "名乗り %s / 実際 %d" % (m6.group(1) if m6 else "無し", len(指せない)))

m3 = re.search(r"外から来て、なお読んでいないものが \*\*(\d+) 件\*\*", errata)
check("ERRATA.md が名乗る借り物の件数が実際と合う",
      m3 is not None and int(m3.group(1)) == len(借り物),
      ("名乗り %s / 実際 %d" % (m3.group(1) if m3 else "無し", len(借り物))))

# E6 の内訳表。**散文に書いた三つの数を、そのまま突き合わせる。**
for 語, 実際 in (("自前", o_tally["自前"]), ("外から", o_tally["外から"]),
                 ("未記載", 未記載)):
    m4 = re.search(r"\| %s \| (\d+) 件" % 語, errata)
    check("ERRATA.md が名乗る「%s」の件数が実際と合う" % 語,
          m4 is not None and int(m4.group(1)) == 実際,
          "名乗り %s / 実際 %d" % (m4.group(1) if m4 else "無し", 実際))

print("\n5. 書棚が作り直せるか")

import subprocess                                    # noqa: E402
before = io.open(os.path.join(ROOT, "SHELF.md"), encoding="utf-8").read() \
    if os.path.exists(os.path.join(ROOT, "SHELF.md")) else None
subprocess.run([sys.executable, os.path.join(HERE, "build_shelf.py")],
               capture_output=True, cwd=ROOT)
after = io.open(os.path.join(ROOT, "SHELF.md"), encoding="utf-8").read()
check("SHELF.md が references.toml から作り直したものと一致する",
      before == after, "python3 verification/build_shelf.py を走らせてください")

m2 = re.search(r"まだ確かめていない (\d+) 冊", after)
check("書棚が名乗る未確認の冊数が実際と合う",
      m2 is not None and int(m2.group(1)) == len(todo),
      "名乗り %s / 実際 %d" % (m2.group(1) if m2 else "無し", len(todo)))

print("\n" + "-" * 58)
print("  記入済み %d 件 / 未記入 %d 件 / 合計 %d 件"
      % (len(done), len(todo), len(refs)))
if failures:
    print("%d 件が通り、%d 件が通りませんでした。" % (passed, len(failures)))
    for f in failures:
        print("  - " + f)
    sys.exit(1)
print("%d 件すべて通りました。" % passed)
