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
check('アスタリスクのまま残った強調がない', emphasis);
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

console.log();
if (failures.length) {
  console.log(failures.length + ' 項目が通りませんでした。');
  process.exit(1);
}
console.log('すべて通りました。');
