import { chromium } from 'playwright';
import { fileURLToPath } from 'url';
import path from 'path';
const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');
const APP = 'file://' + path.join(ROOT, 'app', 'index.html');
const b=await chromium.launch({executablePath: process.env.CHROMIUM || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});
const p=await b.newPage({viewport:{width:1180,height:1100}});
const errs=[]; p.on('pageerror',e=>errs.push('PE:'+e.message));
p.on('console',m=>{if(m.type()==='error')errs.push('CE:'+m.text());});
await p.goto(APP);
await p.evaluate(()=>{startSession(DB.filter(q=>q.theme==='総量規制・過剰貸付けの禁止').slice(0,12),'practice','総量規制・過剰貸付けの禁止');});
await p.waitForTimeout(300);
await p.click('.opt[data-n="1"]'); await p.waitForTimeout(700);
await p.screenshot({path: path.join(ROOT,'dist','shots','v6-q.png'),fullPage:true});
console.log('タグ:',await p.$$eval('.qmeta .tag',n=>n.map(x=>x.textContent.trim())));
console.log('解答後:',await p.$$eval('.after button',n=>n.map(x=>x.textContent.trim())));
// テーマ一覧
await p.click('#homeBtn'); await p.waitForTimeout(300);
await p.click('#allTopics'); await p.waitForTimeout(400);
console.log('テーマ一覧の行数:',(await p.$$('.trow')).length);
await p.screenshot({path: path.join(ROOT,'dist','shots','v6-themes.png'),fullPage:true});
// ダーク
await p.click('#brandBtn'); await p.waitForTimeout(200);
await p.click('#themeBtn'); await p.waitForTimeout(400);
await p.screenshot({path: path.join(ROOT,'dist','shots','v6-dark.png'),fullPage:false});
console.log('ERRORS:',errs.length?errs:'none');
await b.close();
