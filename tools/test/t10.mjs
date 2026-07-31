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
// 履歴を投入して合格可能性・復習期日・週間バーを出す
await p.evaluate(()=>{
  const S={q:{},exams:[],xp:2100,days:{},streak:9,best:14,last:null,badges:{},
           goal:20,combo:0,bestCombo:12,cfg:{n:20,mode:'auto',scope:'all'}};
  const day=86400000, now=Date.now();
  const dk=d=>`${d.getFullYear()}-${d.getMonth()+1}-${d.getDate()}`;
  for(let i=0;i<45;i++){const d=new Date();d.setDate(d.getDate()-i);
    if(i<9||i%3) S.days[dk(d)]=8+Math.floor(Math.random()*22);}
  S.last=dk(new Date());
  DB.slice(0,320).forEach((q,i)=>{
    const wrong = (q.sectionShort==='財務会計'? i%2===0 : i%4===0);
    S.q[q.id]={n:1+(i%3),ng:wrong?1:0,last:now-i*3600e3,flag:i%23===0,
               ease:wrong?2.1:2.6,iv:wrong?0:3,due:now+(wrong?-day:2*day),reps:wrong?0:2};
  });
  localStorage.setItem('kashikin.progress.v3',JSON.stringify(S));
});
await p.reload(); await p.waitForTimeout(500);
console.log('見出し:',(await p.textContent('.why .msg')).replace(/\s+/g,' ').trim());
console.log('合格可能性:',(await p.textContent('.pass .hd')).replace(/\s+/g,' ').trim());
console.log('連続:',(await p.textContent('.srow')).replace(/\s+/g,' ').trim());
console.log('分野別:',await p.$$eval('.secrow',n=>n.map(x=>x.textContent.replace(/\s+/g,' ').trim())));
const w=await p.$$eval('.wk i',n=>n.map(x=>Math.round(x.getBoundingClientRect().height)));
console.log('週バー高さ:',w);
const sw=await p.$$eval('.secrow .swatch',n=>n.map(x=>{const r=x.getBoundingClientRect();return `${Math.round(r.x)},${Math.round(r.width)}x${Math.round(r.height)}`}));
console.log('分野スウォッチ位置:',sw);
console.log('論点の正答率:',await p.$$eval('.trow .acc',n=>n.slice(0,5).map(x=>x.textContent)));
await p.screenshot({path: path.join(ROOT,'dist','shots','v5-home.png'),fullPage:true});
console.log('ERRORS:',errs.length?errs:'none');
await b.close();
