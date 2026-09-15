# -*- coding: utf-8 -*-
"""投稿用の原稿が、公開されている本文と一字一句同じであることを確かめる。

**体裁だけを変えた。**本文は変えていない。それを機械で示す。
落としたものは三つだけで、下に名前で並べてある。
"""
import zipfile, re, io, unicodedata, sys

DOCX = 'submission/celibate-individual-conatus.docx'
SRC  = 'papers/celibate-individual.md'

# **落としたもの。**これ以外は落としていない。
落とした = [
    '扉の著者行（匿名の査読に回るため）',
    '扉の書誌の表（DOI・ライセンス・PDF への参照）',
    '日本語による要旨（誌の言語は英語である）',
]

def docx_text(path):
    d = zipfile.ZipFile(path).read('word/document.xml').decode('utf-8')
    out = []
    for p in re.findall(r'<w:p[ >].*?</w:p>', d, re.S):
        t = ''.join(re.findall(r'<w:t[^>]*>(.*?)</w:t>', p, re.S))
        for a, b in (('&amp;','&'),('&lt;','<'),('&gt;','>'),('&quot;','"'),('&apos;',"'")):
            t = t.replace(a, b)
        if t.strip():
            out.append(t)
    return ''.join(out)

def source_text(path):
    lines = io.open(path, encoding='utf-8').read().split('\n')
    keep, skip = [], False
    for l in lines:
        if l.startswith('## 日本語による要旨'):
            skip = True; continue
        if l.startswith('## Abstract'):
            skip = False
        if skip:
            continue
        keep.append(l)
    b = '\n'.join(keep)
    i = b.find('## Abstract')
    head, rest = b[:i], b[i:]
    title = [l for l in head.split('\n')
             if l.startswith('# ') or (l.startswith('**') and l.endswith('**'))]
    md = '\n\n'.join(title) + '\n\n' + rest
    s = ''.join(l.strip() for l in md.split('\n') if l.strip())
    return s.replace('**', '').replace('## ', '').replace('# ', '')

norm = lambda s: unicodedata.normalize('NFC', re.sub(r'\s+', '', s))
a, b = norm(docx_text(DOCX)), norm(source_text(SRC))

print('落としたもの')
for x in 落とした:
    print('  -', x)
print()
print('原稿   %d 字' % len(a))
print('公開版 %d 字' % len(b))

if a == b:
    print('\n一致した。**本文は一字も変えていない。**')
    sys.exit(0)

for k in range(min(len(a), len(b))):
    if a[k] != b[k]:
        print('\n食い違い 位置 %d' % k)
        print('  原稿   …%s…' % a[max(0,k-60):k+60])
        print('  公開版 …%s…' % b[max(0,k-60):k+60])
        break
else:
    print('\n長さだけが違う。末尾 …%s' % (a if len(a)>len(b) else b)[min(len(a),len(b)):][:80])
sys.exit(1)
