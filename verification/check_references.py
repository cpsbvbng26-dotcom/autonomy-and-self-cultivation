#!/usr/bin/env python3
"""参考文献の宣言が、紙面と食い違っていないかを見る。

    python3 verification/check_references.py

**この検査は「読んだか」を見ない。**内面は外から確かめられない。見るのは
宣言と紙面の整合だけである。

いまはほとんどが空欄で、それが正しい初期状態である（ERRATA の `E6`）。
**空欄であることは失敗ではない。**失敗になるのは、

  - 宣言した典拠が、その論文の紙面に無いとき（でっち上げ）
  - 埋めた項目が、決まりを満たしていないとき
  - **未記入の件数を、散文が実際と違う数で名乗っているとき**

の三つである。**残りが何件かを、機械が数えて散文と突き合わせる。**
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

bad_role = [r["id"] for r in done if r.get("role") not in ROLES]
check("埋めた項目の使い方が決めた語である", not bad_role,
      "、".join(bad_role) or "使えるのは " + "・".join(ROLES))

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

# 参考文献欄にあるだけで、本文から引かれていない項目。
#
# **以前の検査は、参考文献の行に文字列があれば通していた。**本文で使われているかを
# 見ていなかった。実際に一件（Foucault）を見落としていた。
#
# 探索語は id の真ん中から取り、取れないものは body_key を書く。
# **Jünger を junger で探して誤検出した。**綴りは合わせる。

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

print("\n4. 散文が名乗る残り件数")

errata = io.open(os.path.join(ROOT, "ERRATA.md"), encoding="utf-8").read()
m = re.search(r"未記入は \*\*(\d+) 件\*\*", errata)
check("ERRATA.md が名乗る未記入の件数が実際と合う",
      m is not None and int(m.group(1)) == len(todo),
      ("名乗り %s / 実際 %d" % (m.group(1) if m else "無し", len(todo))))

print("\n5. 書棚が作り直せるか")

import subprocess                                    # noqa: E402
before = io.open(os.path.join(ROOT, "SHELF.md"), encoding="utf-8").read() \
    if os.path.exists(os.path.join(ROOT, "SHELF.md")) else None
subprocess.run([sys.executable, os.path.join(HERE, "build_shelf.py")],
               capture_output=True, cwd=ROOT)
after = io.open(os.path.join(ROOT, "SHELF.md"), encoding="utf-8").read()
check("SHELF.md が references.toml から作り直したものと一致する",
      before == after, "python3 verification/build_shelf.py を走らせてください")

m2 = re.search(r"まだ読んでいない (\d+) 冊", after)
check("書棚が名乗る未読の冊数が実際と合う",
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
