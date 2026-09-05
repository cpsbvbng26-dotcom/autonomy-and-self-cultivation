#!/usr/bin/env python3
"""papers/ の Markdown が、pdf/ の PDF と同じ語を同じ順に並べているかを照合する。

README は三篇の語数と差の内訳を表で主張しています。**その数字をここで出しています。**
書き写した値ではありません。

  python3 verification/check_fidelity.py          # 要約だけ
  python3 verification/check_fidelity.py -v       # 食い違いを一件ずつ表示

必要なもの: pypdf（`pip install pypdf`）。

## 何を比べているか

PDF から抽出した語の列と、Markdown 本文の語の列を、`difflib.SequenceMatcher` で突き合わせます。
比べるのは **Abstract 以降**です。Markdown の冒頭には、このリポジトリのために書き下ろした
書誌表と日本語の要旨があり、原文にはありません。

**語の列だけを見て、空白・改行・見出し記号は無視します。** 段落の折り返し位置は組版の産物で、
本文の異同ではないからです。逆に言えば、**語が一つでも増減すれば検出します。**

## 差が出ることが分かっているもの

行末で割れたハイフン語（`non-negotiable` など）を繋ぎ直したもの、および抽出器が括弧の内側に
入れてしまった空白（`( Seelengrund)`）を取り除いたもの。**それ以外の差はありません。**
差の件数が README の表と変われば、このスクリプトは落ちます。
"""

import difflib
import os
import re
import sys

try:
    from pypdf import PdfReader
except ImportError:
    sys.exit("pypdf が要ります: pip install pypdf")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# README の表が主張している値。ここを変えずに本文を変えれば、このスクリプトが落ちる。
PAPERS = [
    {
        "label": "独身論",
        "pdf": "pdf/nobility-and-exemplarity-of-the-celibate-individual-v2.pdf",
        "md": "papers/celibate-individual.md",
        "expected_pdf_words": 3696,
        "expected_matched": 3696,
    },
    {
        "label": "人格的帝国主義",
        "pdf": "pdf/manifesto-of-imperial-selfhood-revised.pdf",
        "md": "papers/imperial-selfhood.md",
        "expected_pdf_words": 4302,
        "expected_matched": 4294,
    },
    {
        "label": "断片主義",
        "pdf": "pdf/fragmentarian-spiritual-individualism.pdf",
        "md": "papers/fragmentarian-spiritual-individualism.md",
        "expected_pdf_words": 5147,
        "expected_matched": 5131,
    },
]

VERBOSE = "-v" in sys.argv or "--verbose" in sys.argv


def words(text):
    """語の列にする。ページ番号だけの行は落とし、空白の種類は問わない。"""
    text = re.sub(r"^\s*\d{1,3}\s*$", "", text, flags=re.M)
    return re.sub(r"[ \t 　]+", " ", text).split()


def from_abstract(text):
    """Abstract の見出しから後ろだけを返す。"""
    m = re.search(r"^\s*(##\s*)?Abstract\s*$", text, flags=re.M)
    if not m:
        sys.exit("Abstract の見出しが見つかりません")
    return text[m.end():]


def pdf_words(path):
    reader = PdfReader(path)
    raw = "\n".join((page.extract_text() or "") for page in reader.pages)
    return words(from_abstract(raw))


def md_words(path):
    with open(path, encoding="utf-8") as fh:
        raw = fh.read()
    body = from_abstract(raw)
    body = re.sub(r"^#+ ", "", body, flags=re.M)          # 見出し記号
    body = re.sub(r"^\*(.+)\*$", r"\1", body, flags=re.M)  # 単独行の強調
    return words(body)


def main():
    rows = []
    failed = []

    for paper in PAPERS:
        src = pdf_words(os.path.join(ROOT, paper["pdf"]))
        out = md_words(os.path.join(ROOT, paper["md"]))

        matcher = difflib.SequenceMatcher(None, src, out, autojunk=False)
        matched = sum(size for _, _, size in matcher.get_matching_blocks())
        diffs = [op for op in matcher.get_opcodes() if op[0] != "equal"]

        ok = (len(src) == paper["expected_pdf_words"]
              and matched == paper["expected_matched"])
        rows.append((paper["label"], len(src), len(out), matched,
                     len(src) - matched, len(diffs), ok))
        if not ok:
            failed.append(paper["label"])

        if VERBOSE and diffs:
            print("--- %s: 食い違い %d 件" % (paper["label"], len(diffs)))
            for op, i1, i2, j1, j2 in diffs:
                print("  [%s] PDF %d-%d: %s" % (op, i1, i2, " ".join(src[i1:i2])[:120]))
                print("      MD  %d-%d: %s" % (j1, j2, " ".join(out[j1:j2])[:120]))
            print()

    width = max(len(r[0]) for r in rows) + 2
    print()
    print("%-*s %8s %8s %8s %8s %8s  %s"
          % (width, "", "PDF 語数", "MD 語数", "一致", "差", "箇所", "判定"))
    print("-" * (width + 56))
    for label, n_src, n_out, matched, gap, n_diffs, ok in rows:
        print("%-*s %8d %8d %8d %8d %8d  %s"
              % (width, label, n_src, n_out, matched, gap, n_diffs,
                 "OK" if ok else "FAIL"))
    print("-" * (width + 56))

    if failed:
        print()
        print("README の表と一致しません: " + "、".join(failed))
        print("本文を変えたのなら README の表も直してください。")
        print("変えていないのなら、抽出結果が変わっています（pypdf の版など）。")
        if not VERBOSE:
            print("-v を付けて実行すると、食い違いを一件ずつ表示します。")
        return 1

    print("README の表のとおりです。")
    if not VERBOSE:
        print("差の中身は -v で表示できます。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
