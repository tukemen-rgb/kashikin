import { chromium } from 'playwright';
import { fileURLToPath } from 'url';
import path from 'path';
const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');
const APP = 'file://' + path.join(ROOT, 'app', 'index.html');
const b=await chromium.launch({executablePath: process.env.CHROMIUM || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});
const errs=[];
const m=await b.newPage({viewport:{width:390,height:844},deviceScaleFactor:2});
m.on('pageerror',e=>errs.push('PE: '+e.message));
m.on('console',x=>{if(x.type()==='error')errs.push('CE: '+x.text());});
await m.goto(APP);
await m.evaluate(()=>{
  const S={q:{},exams:[],xp:2100,days:{},streak:9,best:14,last:null,badges:{},
           goal:20,combo:0,bestCombo:12,cfg:{n:20,mode:'auto',scope:'all'}};
  const day=86400000,now=Date.now(),dk=d=>`${d.getFullYear()}-${d.getMonth()+1}-${d.getDate()}`;
  for(let i=0;i<45;i++){const d=new Date();d.setDate(d.getDate()-i);if(i<9||i%3)S.days[dk(d)]=8+((i*7)%22);}
  S.last=dk(new Date());
  DB.slice(0,320).forEach((q,i)=>{const w=i%4===0;
    S.q[q.id]={n:1+(i%3),ng:w?1:0,last:now-i*3600e3,flag:i%23===0,ease:2.5,iv:w?0:3,due:now+(w?-day:2*day),reps:w?0:2};});
  localStorage.setItem('kashikin.progress.v3',JSON.stringify(S));
});
await m.reload(); await m.waitForTimeout(500);
console.log('横溢れ:',await m.evaluate(()=>document.documentElement.scrollWidth>document.documentElement.clientWidth));
console.log('実績（起動時判定）:',(await m.$$('.badge.on')).length,'/ 12');
await m.screenshot({path: path.join(ROOT,'dist','shots','v5-m-home.png'),fullPage:true});
await m.click('#startBtn'); await m.waitForTimeout(300);
await m.click('.opt[data-n="2"]'); await m.waitForTimeout(600);
await m.screenshot({path: path.join(ROOT,'dist','shots','v5-m-q.png')});
console.log('ERRORS:',errs.length?errs:'none');
await b.close();
