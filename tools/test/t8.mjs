import { chromium } from 'playwright';
import { fileURLToPath } from 'url';
import path from 'path';
const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');
const APP = 'file://' + path.join(ROOT, 'app', 'index.html');
const b=await chromium.launch({executablePath: process.env.CHROMIUM || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});
const errs=[];
// 模試フル
const p=await b.newPage({viewport:{width:1180,height:900}});
p.on('pageerror',e=>errs.push('PE:'+e.message));
p.on('console',m=>{if(m.type()==='error')errs.push('CE:'+m.text());});
await p.goto(APP);
await p.click('[data-go="examPick"]'); await p.waitForTimeout(200);
console.log('模試の選択肢数:',(await p.$$('[data-kai]')).length,'(20回+ランダム=21)');
await p.click('[data-kai="6"]'); await p.waitForTimeout(300);
for(let i=0;i<50;i++){ await p.click(`[data-jump="${i}"]`); await p.click('.opt[data-n="2"]'); }
await p.click('[data-jump="49"]'); await p.click('#submit'); await p.waitForTimeout(400);
console.log('採点:',(await p.textContent('.result .score')).replace(/\s+/g,''),
            (await p.textContent('.stamp')).trim(),'|',(await p.textContent('.result .line')).trim());
console.log('XP表示:',(await p.textContent('.gained').catch(()=>'なし')).trim());
await p.click('#back'); await p.waitForTimeout(300);
const st=await p.$$eval('.stat .v',n=>n.map(x=>x.textContent.trim()));
console.log('ホーム統計:',st);
console.log('段位:',(await p.textContent('.rankseal span')).trim());
console.log('獲得実績:',(await p.$$('.badge.on')).length);
await p.screenshot({path: path.join(ROOT,'dist','shots','v3-home.png'),fullPage:true});
// 今日の10問
await p.click('#startBtn'); await p.waitForTimeout(300);
console.log('学習セッション:',(await p.textContent('.counter')).replace(/\s+/g,' ').trim());
// モバイル
const m=await b.newPage({viewport:{width:390,height:844},deviceScaleFactor:2});
m.on('pageerror',e=>errs.push('MPE:'+e.message));
await m.goto(APP);
await m.waitForTimeout(300);
console.log('モバイル横溢れ:',await m.evaluate(()=>document.documentElement.scrollWidth>document.documentElement.clientWidth));
await m.screenshot({path: path.join(ROOT,'dist','shots','v3-m-home.png'),fullPage:true});
await m.click('#startBtn'); await m.waitForTimeout(300);
await m.screenshot({path: path.join(ROOT,'dist','shots','v3-m-q.png')});
console.log('ERRORS:',errs.length?errs:'none');
await b.close();
