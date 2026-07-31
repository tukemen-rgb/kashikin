import { chromium } from 'playwright';
import { fileURLToPath } from 'url';
import path from 'path';
const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');
const APP = 'file://' + path.join(ROOT, 'app', 'index.html');
const b=await chromium.launch({executablePath: process.env.CHROMIUM || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});
const p=await b.newPage({viewport:{width:1180,height:1000}});
const errs=[]; p.on('pageerror',e=>errs.push('PE: '+e.message));
p.on('console',m=>{if(m.type()==='error')errs.push('CE: '+m.text());});
await p.goto(APP);
await p.waitForTimeout(500);
console.log('CTA:',(await p.textContent('#startBtn')).trim());
console.log('見出し:',(await p.textContent('.why .msg')).replace(/\s+/g,' ').trim());
console.log('曜日セル:',(await p.$$('.day')).length,' 週バー:',(await p.$$('.wk')).length);
console.log('分野行:',(await p.$$('.secrow')).length,' 論点行:',(await p.$$('.trow')).length);
console.log('合格可能性カード:',(await p.$('.pass'))?'あり':'なし（履歴不足で非表示・想定どおり）');
await p.screenshot({path: path.join(ROOT,'dist','shots','v4-home.png'),fullPage:true});
// 学習開始
await p.click('#startBtn'); await p.waitForTimeout(400);
console.log('セッション:',(await p.textContent('.counter')).replace(/\s+/g,' ').trim());
console.log('ナビチップ:',(await p.$$('.nav button')).length);
await p.click('.opt[data-n="1"]'); await p.waitForTimeout(600);
console.log('判定:',(await p.textContent('.verdict')).replace(/\s+/g,' ').trim());
console.log('解答後アクション:',await p.$$eval('.after button',n=>n.map(x=>x.textContent.trim())));
await p.screenshot({path: path.join(ROOT,'dist','shots','v4-q.png'),fullPage:true});
// 類題
const sim=await p.$('#simBtn');
if(sim){await sim.click(); await p.waitForTimeout(300);
  console.log('類題セッション:',(await p.textContent('.counter')).replace(/\s+/g,' ').trim());}
console.log('ERRORS:',errs.length?errs:'none');
await b.close();
