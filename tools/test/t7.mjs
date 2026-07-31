import { chromium } from 'playwright';
import { fileURLToPath } from 'url';
import path from 'path';
const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');
const APP = 'file://' + path.join(ROOT, 'app', 'index.html');
const b=await chromium.launch({executablePath: process.env.CHROMIUM || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});
const p=await b.newPage({viewport:{width:1180,height:1100}});
const errs=[]; p.on('pageerror',e=>errs.push(e.message));
await p.goto(APP);
// 多文の問題を選ぶ
await p.evaluate(()=>{
  const q=DB.filter(x=>(x.stem.match(/。/g)||[]).length>=3)
            .sort((a,c)=>c.stem.length-a.stem.length)[0];
  window.__id=q.id; startSession([q],'practice','多文テスト');
});
await p.waitForTimeout(300);
console.log('多文問題:',await p.evaluate(()=>window.__id),' 文数:',(await p.$$('.stem .s')).length);
await p.screenshot({path: path.join(ROOT,'dist','shots','v2-multi.png'),fullPage:true});
// 本文が一字も変わっていないか検証
const same=await p.evaluate(()=>{
  const q=DB.find(x=>x.id===window.__id);
  const dom=document.querySelector('.stem').textContent;
  return {equal: dom===q.stem, domLen:dom.length, srcLen:q.stem.length};
});
console.log('問題文がDOM上で原文と完全一致:',same);
// 全1000問について、描画テキストが原文と一致するかを一括検証
const all=await p.evaluate(()=>{
  const bad=[];
  const div=document.createElement('div');
  for(const q of DB){
    div.innerHTML=proseHTML(q.stem,{cue:true});
    if(div.textContent!==q.stem) bad.push([q.id,'stem']);
    for(const [k,v] of Object.entries(q.statements)){
      div.innerHTML=proseHTML(v); if(div.textContent!==v) bad.push([q.id,'stmt'+k]);
    }
    for(const [k,v] of Object.entries(q.options)){
      div.innerHTML=proseHTML(v); if(div.textContent!==v) bad.push([q.id,'opt'+k]);
    }
    if(q.note){ div.innerHTML=proseHTML(q.note); if(div.textContent!==q.note) bad.push([q.id,'note']); }
  }
  return bad;
});
console.log('★ 全1000問 描画テキストと原文の不一致:',all.length===0?'0件（完全一致）':all.slice(0,10));
// ○×マーク（記述ａ〜ｄのある回に移ってから確認する）
await p.evaluate(()=>{const q=DB.find(x=>Object.keys(x.statements).length>=4);startSession([q],'practice','記述テスト');});
await p.waitForTimeout(250);
for(let i=0;i<2;i++){ const st=await p.$$('[data-stmt]'); await st[i].click(); await p.waitForTimeout(120); }
console.log('tally:',(await p.textContent('.tally').catch(()=>'なし')).replace(/\s+/g,' ').trim());
await p.screenshot({path: path.join(ROOT,'dist','shots','v2-marks.png'),fullPage:true});
console.log('ERRORS:',errs.length?errs:'none');
await b.close();
