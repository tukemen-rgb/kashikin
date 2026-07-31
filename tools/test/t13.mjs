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
// 弱点が出るように履歴を作る（義務/任意と個数問題と否定形を苦手に）
await p.evaluate(()=>{
  const S={q:{},ms:{},exams:[],xp:1800,days:{},streak:6,best:11,last:null,badges:{},
           goal:20,combo:0,bestCombo:9,cfg:{n:20,mode:'auto',scope:'all'}};
  const day=86400000,now=Date.now(),dk=d=>`${d.getFullYear()}-${d.getMonth()+1}-${d.getDate()}`;
  for(let i=0;i<40;i++){const d=new Date();d.setDate(d.getDate()-i);if(i<6||i%2)S.days[dk(d)]=10+((i*5)%18);}
  S.last=dk(new Date());
  DB.slice(0,300).forEach((q,i)=>{
    let wrong = i%5===0;
    if(q.traps.includes('duty')) wrong = i%3!==0;   // 義務/任意を苦手に
    if(q.format==='count')       wrong = i%2===0;   // 個数問題も苦手に
    if(q.negative)               wrong = wrong || i%4===0;
    S.q[q.id]={n:1,ng:wrong?1:0,last:now-i*3600e3,flag:false,
               ease:2.5,iv:wrong?0:3,due:now+(wrong?-day:2*day),reps:wrong?0:2};
    S.ms[q.id]={t:(i%7===0?15000:60000),c:1};       // 一部を速答に
  });
  localStorage.setItem('kashikin.progress.v3',JSON.stringify(S));
});
await p.reload(); await p.waitForTimeout(400);
await p.click('[data-go="diag"]'); await p.waitForTimeout(400);
console.log('弱点カード:',(await p.$$('.dcard')).length);
console.log(await p.$$eval('.dcard',n=>n.slice(0,6).map(x=>{
  const k=x.querySelector('.dk')?.textContent, t=x.querySelector('.dt')?.textContent,
        v=x.querySelector('.dv')?.textContent, m=x.querySelector('.dm')?.textContent;
  return `[${k}] ${t} ${v} — ${m}`;})));
await p.screenshot({path: path.join(ROOT,'dist','shots','v7-diag.png'),fullPage:true});
// 演習ボタン
const g=await p.$('.dgo');
if(g){await g.click(); await p.waitForTimeout(300);
  console.log('診断からの演習:',(await p.textContent('.counter')).replace(/\s+/g,' ').trim());
  await p.click('.opt[data-n="1"]'); await p.waitForTimeout(600);
  const tr=await p.$('.traps');
  console.log('設問の引っかけ表示:', tr? (await p.textContent('.traps')).replace(/\s+/g,' ').slice(0,120):'なし');
  await p.screenshot({path: path.join(ROOT,'dist','shots','v7-q.png'),fullPage:true});}
console.log('ERRORS:',errs.length?errs:'none');
await b.close();
