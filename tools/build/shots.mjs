// 実機サイズの画面を dist/shots/ に撮る。公開前の目視用。
import { chromium } from 'playwright';
import { fileURLToPath } from 'url';
import path from 'path';
import fs from 'fs';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');
const APP = 'file://' + path.join(ROOT, 'app', 'index.html');
const OUT = path.join(ROOT, 'dist', 'shots');
fs.mkdirSync(OUT, { recursive: true });

const seed = `(() => {
  DB.slice(0, 340).forEach((q, i) => { const c = rec(q.id);
    c.n = 1 + (i % 3); c.ng = (i % 4) ? 1 : 0; c.reps = 1; c.due = Date.now() - 1000; });
  S.xp = 1180; S.streak = 9; S.best = 14; S.bestCombo = 11;
  const d = new Date();
  for (let i = 0; i < 40; i++) { const x = new Date(d); x.setDate(d.getDate() - i);
    S.days[dkey(x)] = 8 + ((i * 7) % 24); }
  S.last = today(); S.exams = [{ title: '第18回', score: 31, pass: 29, at: Date.now() - 8e7 }];
  checkBadges(); save(); renderHome();
})()`;

const b = await chromium.launch({
  executablePath: process.env.CHROMIUM || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
let n = 0;
for (const scheme of ['light', 'dark']) {
  const p = await b.newPage({ viewport: { width: 412, height: 915 }, deviceScaleFactor: 2, colorScheme: scheme });
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto(APP); await p.waitForTimeout(400);
  await p.screenshot({ path: path.join(OUT, `${scheme}-01-初回.png`) }); n++;
  await p.evaluate(seed); await p.waitForTimeout(350);
  await p.screenshot({ path: path.join(OUT, `${scheme}-02-ホーム.png`) }); n++;
  await p.evaluate(() => startSession(pickQuestions(20, 'auto', 'all'), 'practice', '学習'));
  await p.waitForTimeout(300);
  await p.screenshot({ path: path.join(OUT, `${scheme}-03-設問.png`) }); n++;
  await p.evaluate(() => document.querySelectorAll('.opt')[1].click());
  await p.waitForTimeout(700);
  await p.screenshot({ path: path.join(OUT, `${scheme}-04-解答後.png`) }); n++;
  await p.evaluate(() => renderDiag()); await p.waitForTimeout(300);
  await p.screenshot({ path: path.join(OUT, `${scheme}-05-診断.png`) }); n++;
  await p.evaluate(() => renderTopics()); await p.waitForTimeout(300);
  await p.screenshot({ path: path.join(OUT, `${scheme}-06-テーマ.png`) }); n++;
  await p.evaluate(() => renderStats()); await p.waitForTimeout(300);
  await p.screenshot({ path: path.join(OUT, `${scheme}-07-成績.png`), fullPage: true }); n++;
  if (errs.length) { console.error('ERRORS', scheme, errs); process.exit(1); }
  await p.close();
}
await b.close();
console.log(`${n}枚（ライト／ダーク × 7画面）`);
