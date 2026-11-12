/* 生成したサイトを検査する。
 *
 *   node build.js && node verification/check_site.js
 *
 * 依存パッケージなし。ブラウザも起こさない。
 * 生成は成功したように見えて中身が壊れている、という類だけを拾う。
 */

'use strict';

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const ROOT = path.resolve(__dirname, '..');
const SITE = path.join(ROOT, 'site');

let pass = 0;
const failures = [];

function check(label, hits) {
  if (hits.length === 0) { console.log('  OK   ' + label); pass++; return; }
  console.log('  FAIL ' + label + ' — ' + hits.length + ' 件');
  hits.slice(0, 4).forEach((h) => console.log('         ' + h));
  failures.push(label);
}

function walk(dir) {
  return fs.readdirSync(dir, { withFileTypes: true }).flatMap((e) => {
    const full = path.join(dir, e.name);
    return e.isDirectory() ? walk(full) : (full.endsWith('.html') ? [full] : []);
  });
}

if (!fs.existsSync(SITE)) {
  console.error('site/ がありません。先に node build.js を実行してください。');
  process.exit(1);
}

const pages = walk(SITE);
console.log('生成物 ' + pages.length + ' ページを検査します。\n');

/* <style> と <script> の中身は見ない。記法の判定に巻き込まれるため。 */
function bodyOnly(html) {
  return html
    .replace(/<style[\s\S]*?<\/style>/g, '')
    .replace(/<script[\s\S]*?<\/script>/g, '')
    .replace(/<pre[\s\S]*?<\/pre>/g, '')
    .replace(/<code[\s\S]*?<\/code>/g, '');
}

const emphasis = [], links = [], external = [];
for (const file of pages) {
  const rel = path.relative(ROOT, file);
  const body = bodyOnly(fs.readFileSync(file, 'utf8'));
  for (const m of body.matchAll(/\*[^*\s<][^*<\n]{0,60}\*/g)) emphasis.push(rel + ': ' + m[0]);
  for (const m of body.matchAll(/\[[^\]\n]{1,80}\]\([^)\s]{1,200}\)/g)) links.push(rel + ': ' + m[0]);
  for (const m of body.matchAll(/<img[^>]+src="https?:\/\/([^/"]+)/g)) external.push(rel + ': ' + m[1]);
}
/* リポジトリの中のファイルへのリンク（GitHub の URL）は、実在するファイルを指す。../ を残さない。 */
const blob = [];
for (const file of pages) {
  const rel = path.relative(ROOT, file);
  for (const m of fs.readFileSync(file, 'utf8').matchAll(/href="https:\/\/github\.com\/cpsbvbng26-dotcom\/autonomy-and-self-cultivation\/blob\/main\/([^"#]+)/g)) {
    const p = decodeURIComponent(m[1]);
    if (p.split('/').includes('..') || !fs.existsSync(path.join(ROOT, p))) blob.push(rel + ': ' + m[1]);
  }
}
check('アスタリスクのまま残った強調がない', emphasis);
check('リポジトリの中のファイルへのリンクが、実在するファイルを指す', blob);
check('Markdown のまま残ったリンク記法がない', links);
check('外部ホストから画像を読み込んでいない', external);

/* 三篇の全文がすべて出ていること */
const papers = ['celibate-individual', 'imperial-selfhood', 'fragmentarian-spiritual-individualism'];
const missingPapers = papers.filter(
  (n) => !pages.some((f) => path.basename(f) === n + '.html')
);
check('三篇の全文ページが生成されている', missingPapers);

/* Content-Security-Policy。build.js が生成のたびに埋める。 */
const shaOf = (t) => "'sha256-" + crypto.createHash('sha256').update(t, 'utf8').digest('base64') + "'";
const hashesIn = (html, tag) => {
  const re = new RegExp('<' + tag + '(?![^>]*\\bsrc=)[^>]*>([\\s\\S]*?)</' + tag + '>', 'g');
  const out = []; let m;
  while ((m = re.exec(html)) !== null) out.push(shaOf(m[1]));
  return out;
};

const noCsp = [], weak = [], mismatch = [];
for (const file of pages) {
  const html = fs.readFileSync(file, 'utf8');
  const rel = path.relative(ROOT, file);
  const m = /<meta http-equiv="Content-Security-Policy" content="([^"]*)">/.exec(html);
  if (!m) { noCsp.push(rel); continue; }
  const csp = m[1];
  if (csp.indexOf("default-src 'none'") !== 0) weak.push(rel + ": default-src が 'none' でない");
  if (/unsafe-inline|unsafe-eval|unsafe-hashes|\*/.test(csp)) weak.push(rel + ': 緩められている');
  for (const h of hashesIn(html, 'style').concat(hashesIn(html, 'script'))) {
    if (csp.indexOf(h) < 0) mismatch.push(rel);
  }
}
check('すべてのページに CSP がある', noCsp);
check('CSP が緩められていない', weak);
check('CSP のハッシュがページの中身と一致する', [...new Set(mismatch)]);

/* ================================================================ *
 * 読むための案内（README・docs/claims.md・docs/glossary.md）
 *
 * 散文に書いた数と引用を、紙面と記録から数え直して突き合わせる（決めごと 5）。
 * ================================================================ */

const readText = (rel) => fs.readFileSync(path.join(ROOT, rel), 'utf8');
const README = readText('README.md');
const PAPER = {
  N: { short: '独身論', slug: 'celibate-individual' },
  M: { short: '皇帝主義', slug: 'imperial-selfhood' },
  F: { short: '断章論', slug: 'fragmentarian-spiritual-individualism' }
};
const byShort = (s) => Object.keys(PAPER).find((k) => PAPER[k].short === s);
const paperMd = (k) => readText(path.join('papers', PAPER[k].slug + '.md'));
const flat = (t) => String(t).replace(/\s+/g, ' ').trim();
/* README の中の、ある見出しから次の同じ深さの見出しまで。 */
function block(text, heading) {
  const i = text.indexOf('\n' + heading + '\n');
  if (i < 0) return '';
  const level = heading.match(/^#+/)[0].length;
  const rest = text.slice(i + heading.length + 2);
  const m = new RegExp('\\n#{1,' + level + '} ').exec('\n' + rest);
  return m ? rest.slice(0, m.index) : rest;
}
/* 紙面の節。「第3節」「第2.1節」「要旨」「結論」を見出しに引き当て、次の見出しまでを返す。 */
function section(k, label) {
  const md = paperMd(k);
  let re;
  if (label === '要旨') re = /^## Abstract$/m;
  else if (label === '結論') re = /^## (\d+\. )?Conclusion$/m;
  else {
    const m = /^第(\d+)(?:\.(\d+))?節$/.exec(label);
    if (!m) return null;
    re = m[2] ? new RegExp('^### ' + m[1] + '\\.' + m[2] + ' ', 'm') : new RegExp('^## ' + m[1] + '\\. ', 'm');
  }
  const h = re.exec(md);
  if (!h) return null;
  const level = h[0].match(/^#+/)[0].length;
  const rest = md.slice(h.index + h[0].length);
  const e = new RegExp('\\n#{1,' + level + '} ').exec(rest);
  return flat(e ? rest.slice(0, e.index) : rest);
}
const quotes = (t) => [...t.matchAll(/`([^`]+)`/g)].map((m) => m[1]);
const tableRows = (t) => t.split('\n').filter((l) => l.startsWith('|') && !/^\|[\s:|-]+\|$/.test(l))
  .slice(1).map((l) => l.split('|').slice(1, -1).map((c) => c.trim()));

/* 1. 種類と状態の札。引用情報の type。Zenodo の記録が三篇の DOI を IsSupplementTo で指していること。 */
{
  const hits = [];
  const lines = README.split('\n');
  if (!(/^# /.test(lines[0]) && lines[1] === '' && lines[2] === '種類：エッセイ　状態：凍結')) hits.push('README の 3 行目: ' + lines[2]);
  const cff = readText('CITATION.cff');
  if (!/^type: dataset$/m.test(cff)) hits.push('CITATION.cff の type');
  const dois = [...cff.matchAll(/^    doi: (10\.5281\/zenodo\.\d+)$/gm)].map((m) => m[1]).sort();
  const z = JSON.parse(readText('.zenodo.json'));
  const rel = (z.related_identifiers || []).filter((r) => r.relation === 'isSupplementTo').map((r) => r.identifier).sort();
  if (dois.length !== 3 || dois.join() !== rel.join()) hits.push('引用情報の三篇 ' + dois.join(' ') + ' / Zenodo の isSupplementTo ' + rel.join(' '));
  if ((z.related_identifiers || []).some((r) => ['isSupplementTo', 'isDerivedFrom'].indexOf(r.relation) < 0)) hits.push('決めた二つ以外の関係がある');
  check('題の下に種類と状態の札があり、引用情報の type と、Zenodo の記録が三篇を指す関係が揃っている', hits);
}

/* 2. 平易な三行。三篇のそれぞれに、ちょうど三行。 */
{
  const hits = [];
  const 三篇 = block(README, '## 三篇');
  const parts = 三篇.split(/\n### /).slice(1);
  if (parts.length !== 3) hits.push('三篇の節が ' + parts.length);
  for (const p of parts) {
    const i = p.indexOf('\n平易に三行で書きます。\n');
    const rows = i < 0 ? [] : p.slice(i).split('\n\n')[1].split('\n').filter((l) => l.startsWith('- '));
    if (rows.length !== 3) hits.push(p.split('\n')[0].slice(0, 40) + ': ' + rows.length + ' 行');
  }
  check('三篇のそれぞれに、平易な三行がある', hits);
}

/* 3. 呼び名。表の英語の題が引用情報の題と、略号が正誤表の略号と合うこと。
 *    表に無い呼び名が、散文とサイトの見出しに出ていないこと。止める呼び名はここにだけ置く。 */
{
  const hits = [];
  const rows = tableRows(block(README, '## 呼び名'));
  const cff = flat(readText('CITATION.cff'));
  const errata = readText('ERRATA.md');
  for (const [en, , short, k] of rows) {
    if (!PAPER[k] || PAPER[k].short !== short) hits.push('略称と略号: ' + short + ' / ' + k);
    if (cff.indexOf('title: >- ' + en) < 0) hits.push('引用情報に無い題: ' + en);
    if (errata.indexOf('| **' + k + '** | ' + en) < 0) hits.push('正誤表の略号の表と違う: ' + k);
  }
  if (rows.length !== 3) hits.push('行の数 ' + rows.length);
  const 止める = [/断片主義(?!的精神的個人主義)/, /独身と自己陶冶/, /独身者論/, /個人帝国主義/];
  const files = ['README.md', 'ERRATA.md', 'SHELF.md', path.join('papers', 'README.md')]
    .concat(fs.readdirSync(path.join(ROOT, 'docs')).filter((f) => f.endsWith('.md')).map((f) => path.join('docs', f)));
  for (const f of files) {
    readText(f).split('\n').forEach((l, i) => 止める.forEach((re) => { const m = re.exec(l); if (m) hits.push(f + ':' + (i + 1) + ' ' + m[0]); }));
  }
  for (const file of pages) {
    const nav = (/<nav class="nav">([\s\S]*?)<\/nav>/.exec(fs.readFileSync(file, 'utf8')) || [, ''])[1];
    止める.forEach((re) => { const m = re.exec(nav); if (m) hits.push(path.relative(ROOT, file) + ' の見出し ' + m[0]); });
    for (const k of Object.keys(PAPER)) if (nav.indexOf('>' + PAPER[k].short + '</a>') < 0) hits.push(path.relative(ROOT, file) + ' の見出しに ' + PAPER[k].short + ' が無い');
  }
  check('呼び名が表の名だけで、表が引用情報と正誤表に合う', [...new Set(hits)]);
}

/* 4. 主張と覆し方。記号が骨格にあり、落ちる節が紙面にあり、引いた句がその節にあること。 */
{
  const hits = [];
  const doc = readText(path.join('docs', 'claims.md'));
  const 骨格 = block(README, '## 三篇の骨格');
  const rows = tableRows(block(doc, '## 三篇の主張と覆し方'));
  for (const [short, claim, cond, sec] of rows) {
    const k = byShort(short);
    if (!k) { hits.push('論文の名: ' + short); continue; }
    const m = /^(P\d+[a-c]?|C\d?) /.exec(claim);
    if (m) {
      const sk = block(骨格, '### ' + short);
      if (!new RegExp('^\\| \\**' + m[1] + '\\** \\|', 'm').test(sk)) hits.push(short + ' の骨格に ' + m[1] + ' が無い');
    }
    const body = section(k, sec);
    if (body === null) { hits.push(short + ' に ' + sec + ' が無い'); continue; }
    quotes(cond).forEach((q) => { if (body.indexOf(flat(q)) < 0) hits.push(short + ' ' + sec + ' に無い句: ' + q); });
  }
  if (rows.length === 0) hits.push('表が無い');
  check('主張と覆し方の表が、骨格の記号と紙面の節と句に合う', hits);
}

/* 5. 言っていないこと。引いた句がその節にあり、正誤表の番号が正誤表にあること。 */
{
  const hits = [];
  const doc = readText(path.join('docs', 'claims.md'));
  const 区 = block(doc, '## この稿が言っていないこと');
  const errata = readText('ERRATA.md');
  let n = 0;
  for (const k of Object.keys(PAPER)) {
    const items = block(区, '### ' + PAPER[k].short).split('\n').filter((l) => l.startsWith('- '));
    if (!items.length) hits.push(PAPER[k].short + ' の節が無い');
    for (const l of items) {
      n++;
      const loc = (/（([^（）]+)）$/.exec(l) || [, ''])[1];
      const e = /^ERRATA の ([EN]\d+)$/.exec(loc);
      if (e) { if (!new RegExp('^#{2,3} ' + e[1] + ' —', 'm').test(errata)) hits.push('正誤表に無い番号: ' + e[1]); continue; }
      const body = section(k, loc);
      if (body === null) { hits.push(PAPER[k].short + ' に ' + loc + ' が無い'); continue; }
      const qs = quotes(l);
      if (!qs.length) hits.push('句も正誤表の番号も無い行: ' + l.slice(0, 30));
      qs.forEach((q) => { if (body.indexOf(flat(q)) < 0) hits.push(PAPER[k].short + ' ' + loc + ' に無い句: ' + q); });
    }
  }
  check('「この稿が言っていないこと」の句と番号が、紙面と正誤表にある', hits);
}

/* 6. 用語集。根拠の句がその節にあり、「出てくる論文」が数え直したものと合うこと。 */
{
  const hits = [];
  const doc = readText(path.join('docs', 'glossary.md'));
  const span = (k) => { const md = paperMd(k); return md.slice(md.indexOf('\n## Abstract'), md.indexOf('\n## References')); };
  const rows = doc.split('\n').filter((l) => /^\| [^-|]/.test(l) && l.indexOf('| 語 |') !== 0)
    .map((l) => l.split('|').slice(1, -1).map((c) => c.trim()));
  for (const [ja, term, , basis, where] of rows) {
    const t = term.replace(/`/g, '');
    const re = new RegExp('\\b' + t.replace(/[-]/g, '\\-') + 's?\\b', 'i');
    const got = Object.keys(PAPER).filter((k) => re.test(span(k))).join('・');
    if (got !== where) hits.push(ja + ' 名乗り ' + where + ' / 実際 ' + got);
    const m = /`([^`]+)`（([NMF]) ([^）]+)）$/.exec(basis);
    if (!m) { hits.push(ja + ' の根拠の形'); continue; }
    const body = section(m[2], m[3]);
    if (body === null || body.indexOf(flat(m[1])) < 0) hits.push(ja + ' の根拠が ' + m[2] + ' ' + m[3] + ' に無い');
  }
  if (rows.length === 0) hits.push('表が無い');
  check('用語集の根拠の句が紙面にあり、出てくる論文が数え直したものと合う', hits);
}

/* 7. 読む時間の目安。build.js が語数から数える。同じ数え方で数え直す。 */
{
  const hits = [];
  const words = (k) => {
    const md = paperMd(k);
    return md.slice(md.indexOf('\n## Abstract'), md.indexOf('\n## References'))
      .replace(/^#+ .*$/gm, '').replace(/[*_`|>#]/g, ' ').split(/\s+/)
      .filter((w) => /[A-Za-z0-9À-ɏ]/.test(w)).length;
  };
  const line = (k) => '<p class="reading-time">読むのにかかる時間の目安は約 ' + Math.ceil(words(k) / 200)
    + ' 分です（要旨から参考文献欄の手前までの ' + words(k) + ' 語を、一分に 200 語として build.js が数えました）。</p>';
  const index = fs.readFileSync(path.join(SITE, 'index.html'), 'utf8');
  for (const k of Object.keys(PAPER)) {
    const page = fs.readFileSync(path.join(SITE, 'papers', PAPER[k].slug + '.html'), 'utf8');
    if (page.indexOf(line(k)) < 0) hits.push(PAPER[k].slug + '.html');
    if (index.indexOf(line(k)) < 0) hits.push('index.html の ' + PAPER[k].short);
    if (README.indexOf('<!-- 読む時間:' + PAPER[k].slug + ' -->') < 0) hits.push('README の印 ' + PAPER[k].slug);
  }
  check('読む時間の目安が、三篇の語数から数え直したものと合う', hits);
}

/* 8. まだ確かめていない典拠。論文ごとの数と、別に挙げた id が references.toml と合うこと。 */
{
  const hits = [];
  const toml = readText(path.join('verification', 'references.toml'));
  const arr = (key) => JSON.parse((new RegExp('^' + key + ' = (\\[.*\\])$', 'm').exec(toml) || [, '[]'])[1]);
  const refs = toml.split(/^\[\[reference\]\]\s*$/m).slice(1).map((b) => {
    const v = (key) => (new RegExp('^' + key + ' = "(.*)"$', 'm').exec(b) || [, ''])[1];
    return { id: v('id'), paper: v('paper'), locus: v('locus'), agreement: v('agreement'), origin: v('origin') };
  });
  const rows = tableRows(block(README, '## まだ確かめていない典拠'));
  for (const [short, all, done, todo] of rows) {
    const k = byShort(short);
    const mine = refs.filter((r) => r.paper === k);
    const ok = mine.filter((r) => r.locus && r.agreement).length;
    if (Number(all) !== mine.length || Number(done) !== ok || Number(todo) !== mine.length - ok) {
      hits.push(short + ' 名乗り ' + [all, done, todo].join('/') + ' / 実際 ' + [mine.length, ok, mine.length - ok].join('/'));
    }
  }
  if (rows.length !== 3) hits.push('行の数 ' + rows.length);
  const 区 = block(README, '## まだ確かめていない典拠');
  const ids = (prefix) => (区.split('\n').find((l) => l.startsWith('- ' + prefix)) || '').match(/[NMF]-[a-z]+-\d+/g) || [];
  const want = (a, b, label) => { if (a.slice().sort().join() !== b.slice().sort().join()) hits.push(label + ' 名乗り ' + a.join(' ') + ' / 実際 ' + b.join(' ')); };
  want(ids('着想が典拠の側から'), refs.filter((r) => r.origin === '外から' && !r.agreement).map((r) => r.id), '外から');
  want(ids('読んでいながら'), arr('read_no_locus'), '箇所を指せない');
  want(ids('参考文献欄にあるが'), arr('body_absent'), '本文に無い');
  if (arr('body_only').join() !== 'F:Nitobe' || 区.indexOf('断章論の新渡戸稲造です（`E9`）') < 0) hits.push('本文だけに出る名');
  check('まだ確かめていない典拠の数と挙げた id が、references.toml と合う', hits);
}

/* 8b. 改訂版の計画（docs/revised-editions.md）。2026-11-12 に二段の計画を採り、改訂版を出していないと名乗り、
 *     決めたことの節を持ち、紙面を差し替えないと書き、表が正誤表の項目を過不足なく一度ずつ挙げ、
 *     段の欄が決めた三つのどれかであること。案の印は残さない。 */
{
  const hits = [];
  const doc = readText(path.join('docs', 'revised-editions.md'));
  const errata = readText('ERRATA.md');
  if (doc.split('\n')[2] !== '2026-11-12 に、二つの段に分ける計画を採りました。改訂版は、まだ出していません。') hits.push('冒頭に、計画を採った日と、出していないという断りが無い');
  if (/案（/.test(doc) || doc.indexOf('\n## 決めたこと\n\n2026-11-12 に、次のとおり決めました。\n') < 0 || doc.indexOf('\n改訂版は、段 1 も段 2 も出していません。\n') < 0) hits.push('決めたことの節が無いか、案の印が残っている');
  if (doc.indexOf('\n公開済みの PDF は差し替えません。\n') < 0) hits.push('紙面を差し替えないという一文が無い');
  const want = [...errata.matchAll(/^#{2,3} ([EN]\d+) —/gm)].map((m) => m[1]);
  const rows = tableRows(block(doc, '## 正誤表の項目ごとの扱い'));
  const got = rows.map((r) => r[0]);
  if (JSON.stringify(got) !== JSON.stringify(want)) hits.push('表 ' + got.join(' ') + ' / 正誤表 ' + want.join(' '));
  rows.forEach((r) => { if (r.length !== 4 || ['段 1', '段 2', '—'].indexOf(r[3]) < 0) hits.push('段の欄: ' + r.join(' | ')); });
  const conds = tableRows(block(doc, '## 二つの段に分ける'));
  const shorts = Object.keys(PAPER).map((k) => PAPER[k].short);
  if (JSON.stringify(conds.map((r) => r[0]).sort()) !== JSON.stringify(shorts.slice().sort())) hits.push('段 2 の条件の篇: ' + conds.map((r) => r[0]).join(' '));
  const toml = readText(path.join('verification', 'references.toml'));
  for (const id of doc.match(/`[NMF]-[a-z]+-\d+`/g) || []) {
    if (toml.indexOf('id = "' + id.slice(1, -1) + '"') < 0) hits.push('references.toml に無い id: ' + id);
  }
  if (README.indexOf('| [docs/revised-editions.md](docs/revised-editions.md) |') < 0) hits.push('README の構成の表から指していない');
  check('改訂版の計画が、採った日と出していないことを名乗り、正誤表の項目を一度ずつ挙げている', hits);
}

/* 9. 外部の反応。外部評価の記録から写す。兄弟ディレクトリに cpsbvbng26-dotcom があれば
 *    （ECOSYSTEM_ROOT でも指せる）、三篇の行が過不足なく、欄の最初の一文が同じであることを見る。 */
{
  const SRC = 'https://github.com/cpsbvbng26-dotcom/cpsbvbng26-dotcom/blob/main/docs/external-evaluations.md';
  const hits = [];
  const 区 = block(README, '## 外部の反応');
  if (区.indexOf('](' + SRC + ')') < 0) hits.push('記録へのリンクが無い');
  const eco = process.env.ECOSYSTEM_ROOT || path.resolve(ROOT, '..');
  const f = path.join(eco, 'cpsbvbng26-dotcom', 'docs', 'external-evaluations.md');
  const EN = { N: 'The Nobility and Exemplarity of the Celibate Individual', M: 'Manifesto of Imperial Selfhood', F: 'Fragmentarian Spiritual Individualism' };
  const first = (c) => { const s = c.replace(/\*\*/g, ''); const i = s.indexOf('。'); return i < 0 ? s : s.slice(0, i + 1); };
  if (fs.existsSync(f)) {
    const t = fs.readFileSync(f, 'utf8');
    const table = (h) => {
      const ls = t.slice(t.indexOf(h)).split('\n');
      const k = ls.findIndex((l) => l.startsWith('|'));
      const out = [];
      let prev = null;
      for (let j = k + 2; j < ls.length && ls[j].startsWith('|'); j++) {
        const r = ls[j].split('|').slice(1, -1).map((c) => c.trim());
        if (r[0] === '同上' && prev) r[0] = prev;
        prev = r[0];
        out.push(r);
      }
      return out;
    };
    const 受 = table('## 受けた評価');
    const 出 = table('## 出した先');
    for (const k of Object.keys(PAPER)) {
      const want = 受.filter((r) => r[2].indexOf(EN[k]) === 0).map((r) => [r[0], '受けた評価', first(r[5])])
        .concat(出.filter((r) => r[1] === EN[k]).map((r) => [r[0], '出した先', first(r[3])]))
        .map((r) => r.join(' | '));
      const got = tableRows(block(区, '### ' + PAPER[k].short)).map((r) => r.join(' | '));
      want.filter((x) => got.indexOf(x) < 0).forEach((x) => hits.push(PAPER[k].short + ' に無い行: ' + x));
      got.filter((x) => want.indexOf(x) < 0).forEach((x) => hits.push(PAPER[k].short + ' の記録に無い行: ' + x));
    }
  } else {
    for (const k of Object.keys(PAPER)) if (!tableRows(block(区, '### ' + PAPER[k].short)).length) hits.push(PAPER[k].short + ' の表が無い');
  }
  check('外部の反応が、外部評価の記録と合う' + (fs.existsSync(f) ? '' : '（兄弟に記録が無いので、所在と表の有無だけを見た）'), hits);
}

/* 10. 読みやすさと配信。autonomy-and-self-cultivation と justice-and-algorithms の check_site.js に同じ形で置く。
 * 配色の比（WCAG）、端末の設定に従う暗い配色、画像の代替テキスト、頁の重さ、頁の下の欄、
 * sitemap.xml と robots.txt、正の URL（canonical）。文字を 200% にしたときと 360px の幅は、
 * ブラウザを起こす check_keyboard.js が測る。 */
{
  /* 配信先は build.js が持つ。リポジトリの名から組んだ URL と同じであることも見る。 */
  const src = fs.readFileSync(path.join(ROOT, 'build.js'), 'utf8');
  const BASE = (/const BASE = '([^']+)'/.exec(src) || [])[1] || '';
  const NAME = (/const REPO = 'https:\/\/github\.com\/cpsbvbng26-dotcom\/([^']+)'/.exec(src) || [])[1] || '';
  check('配信先が、このリポジトリの Pages の URL である', BASE && BASE === 'https://cpsbvbng26-dotcom.github.io/' + NAME + '/' ? [] : ['BASE ' + BASE + ' / REPO ' + NAME]);
  /* 一頁の HTML の上限。PDF は読みに行く人だけが落とすので数えない。通信の遅い人のために、
   * いちばん重い頁の倍ほどに置いた。 */
  const MAX_BYTES = 100 * 1000;
  const css = fs.readFileSync(path.join(ROOT, 'assets', 'style.css'), 'utf8');
  const tokens = (m) => (m ? Object.fromEntries([...m[1].matchAll(/--([a-z-]+):\s*(#[0-9a-fA-F]{6})\s*;/g)].map((x) => [x[1], x[2].toLowerCase()])) : null);
  const light = tokens(css.match(/^:root \{([^}]*)\}/m));
  const dark = tokens(css.match(/^:root\[data-theme="dark"\] \{([^}]*)\}/m));
  const media = tokens(css.match(/@media \(prefers-color-scheme: dark\) \{\s*:root:not\(\[data-theme="light"\]\) \{([^}]*)\}/));
  const lum = (hex) => {
    const v = [1, 3, 5].map((i) => parseInt(hex.slice(i, i + 2), 16) / 255).map((c) => (c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4)));
    return 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2];
  };
  const ratio = (a, b) => { const x = lum(a), y = lum(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); };

  const low = [];
  for (const [name, t] of [['ライト', light], ['ダーク', dark]]) {
    if (!t) { low.push(name + 'の定義が無い'); continue; }
    for (const ground of ['bg', 'card']) for (const ink of ['text', 'muted', 'faint', 'accent']) {
      const r = t[ink] && t[ground] ? ratio(t[ink], t[ground]) : 0;
      if (r < 4.5) low.push(name + ' --' + ink + ' / --' + ground + ' ' + r.toFixed(2) + ':1');
    }
  }
  check('文字の色が、地の色に対して WCAG の 4.5:1 以上ある（ライトとダーク）', low);

  const themeHits = [];
  if (!media) themeHits.push('@media (prefers-color-scheme: dark) の定義が無い');
  else if (JSON.stringify(media) !== JSON.stringify(dark)) themeHits.push('端末の設定の暗い配色と、切り替えの暗い配色が違う');
  for (const file of pages) {
    const html = fs.readFileSync(file, 'utf8');
    if (html.indexOf('id="themeToggle"') < 0 || html.indexOf('assets/theme.js"></script>') < 0) themeHits.push(path.relative(SITE, file) + ' に切り替えが無い');
  }
  check('暗い配色は、端末の設定にも切り替えにも従い、二つが同じ色を使う', themeHits);

  const altHits = [];
  for (const file of pages) {
    for (const m of fs.readFileSync(file, 'utf8').matchAll(/<img\b[^>]*>/g)) {
      const alt = /\balt="([^"]*)"/.exec(m[0]);
      const rel = path.relative(SITE, file);
      if (!alt) altHits.push(rel + ' alt が無い');
      else if (/^(画像|写真|図)|^(image|picture|photo)\b/i.test(alt[1]) || /\.(png|jpe?g|svg|gif|webp)$/i.test(alt[1])) altHits.push(rel + ' 「' + alt[1] + '」');
    }
  }
  check('画像の代替テキストが、CONTRIBUTING.md の決めに沿う（「画像」で始めない、ファイル名にしない）', altHits);

  const heavy = pages.map((f) => [path.relative(SITE, f), fs.statSync(f).size]).filter(([, n]) => n > MAX_BYTES).map(([f, n]) => f + ' ' + n + ' バイト');
  check('どの頁の HTML も ' + MAX_BYTES + ' バイト以下', heavy);

  const footHits = [];
  for (const file of pages) {
    const html = fs.readFileSync(file, 'utf8');
    const foot = (/<footer>([\s\S]*?)<\/footer>/.exec(html) || ['', ''])[1];
    const rel = path.relative(SITE, file);
    if (foot.indexOf('運営 根本卓哉') < 0) footHits.push(rel + ' 運営');
    if (foot.indexOf('/issues/new?template=error-report.yml">連絡') < 0) footHits.push(rel + ' 連絡');
    if (foot.indexOf('cpsbvbng26-dotcom/blob/main/DISCLAIMER.md">免責事項') < 0) footHits.push(rel + ' 免責');
    if (/nusquama/i.test(html)) footHits.push(rel + ' 創作のサイトへつないでいる');
  }
  check('どの頁の下の欄にも、運営・連絡・免責があり、創作のサイトへはつながない', footHits);

  const rels = pages.map((f) => path.relative(SITE, f).split(path.sep).join('/'));
  const canonHits = [];
  for (const file of pages) {
    const rel = path.relative(SITE, file).split(path.sep).join('/');
    const want = rel === 'index.html' ? BASE : BASE + rel;
    const got = [...fs.readFileSync(file, 'utf8').matchAll(/<link rel="canonical" href="([^"]+)">/g)].map((m) => m[1]);
    if (got.length !== 1 || got[0] !== want) canonHits.push(rel + ' ' + (got.join(' ') || '無い'));
  }
  check('どの頁にも、正の URL（canonical）がちょうど一つあり、配信先の自分を指す', canonHits);

  const mapHits = [];
  const sm = fs.existsSync(path.join(SITE, 'sitemap.xml')) ? fs.readFileSync(path.join(SITE, 'sitemap.xml'), 'utf8') : '';
  const locs = [...sm.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => m[1]).sort();
  const want = rels.filter((r) => r !== 'CLAUDE.html').map((r) => (r === 'index.html' ? BASE : BASE + r)).sort();
  if (JSON.stringify(locs) !== JSON.stringify(want)) mapHits.push('sitemap.xml ' + locs.length + ' 件 / 頁 ' + want.length + ' 件');
  const robots = fs.existsSync(path.join(SITE, 'robots.txt')) ? fs.readFileSync(path.join(SITE, 'robots.txt'), 'utf8') : '';
  if (robots.indexOf('Sitemap: ' + BASE + 'sitemap.xml') < 0) mapHits.push('robots.txt が sitemap.xml を指していない');
  check('sitemap.xml が CLAUDE.html のほかの全頁を挙げ、robots.txt がそれを指す', mapHits);
}

console.log();
if (failures.length) {
  console.log(failures.length + ' 項目が通りませんでした。');
  process.exit(1);
}
console.log('すべて通りました。');
