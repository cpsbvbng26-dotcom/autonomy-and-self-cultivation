const fs = require('fs');
const { Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType } = require('docx');

const md = fs.readFileSync('manuscript.md', 'utf8').split('\n');

const FONT = 'Times New Roman';
const SZ = 24;   /* half-points = 12pt */

/* **太字の記法だけを解く。**本文の文字は一つも変えない。 */
function runs(text) {
  const out = [];
  const re = /\*\*(.+?)\*\*/g;
  let last = 0, m;
  while ((m = re.exec(text)) !== null) {
    if (m.index > last) out.push(new TextRun({ text: text.slice(last, m.index), font: FONT, size: SZ }));
    out.push(new TextRun({ text: m[1], bold: true, font: FONT, size: SZ }));
    last = re.lastIndex;
  }
  if (last < text.length) out.push(new TextRun({ text: text.slice(last), font: FONT, size: SZ }));
  return out.length ? out : [new TextRun({ text, font: FONT, size: SZ })];
}

const P = (text, opt = {}) => new Paragraph(Object.assign({
  children: runs(text),
  alignment: AlignmentType.JUSTIFIED,
  spacing: { line: 240, lineRule: 'auto', after: 160 },
}, opt));

const children = [];
let title = true;
for (const raw of md) {
  const l = raw.trim();
  if (!l) continue;
  if (l.startsWith('# ')) {
    children.push(new Paragraph({
      children: [new TextRun({ text: l.slice(2), bold: true, font: FONT, size: 28 })],
      alignment: AlignmentType.CENTER, spacing: { after: 160 },
    }));
    continue;
  }
  if (l.startsWith('## ')) {
    title = false;
    children.push(new Paragraph({
      children: [new TextRun({ text: l.slice(3), bold: true, font: FONT, size: SZ })],
      heading: HeadingLevel.HEADING_1,
      alignment: AlignmentType.LEFT, spacing: { before: 280, after: 140 },
    }));
    continue;
  }
  if (title && l.startsWith('**') && l.endsWith('**')) {
    children.push(new Paragraph({
      children: [new TextRun({ text: l.slice(2, -2), italics: true, font: FONT, size: SZ })],
      alignment: AlignmentType.CENTER, spacing: { after: 320 },
    }));
    continue;
  }
  children.push(P(l));
}

const doc = new Document({
  styles: { default: { document: { run: { font: FONT, size: SZ } } } },
  sections: [{
    properties: { page: { margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } } },
    children,
  }],
});

Packer.toBuffer(doc).then((b) => { fs.writeFileSync('celibate-individual-conatus.docx', b); console.log('書き出した', b.length, 'バイト'); });
