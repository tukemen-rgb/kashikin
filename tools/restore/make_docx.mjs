// 令和元年〜令和5年（第14〜18回）を、検証済みデータから作り直す。
// 問題文・記述・選択肢・注記は公式PDFの原文そのまま。正解は公式正答PDF。
import fs from 'fs';
import {
  Document, Packer, Paragraph, TextRun, HeadingLevel, PageBreak,
  Table, TableRow, TableCell, WidthType, ShadingType, AlignmentType, BorderStyle,
} from 'docx';

const DB = JSON.parse(fs.readFileSync('/home/user/kashikin/data/questions.json', 'utf8'));
const TRAPS = Object.fromEntries(
  JSON.parse(fs.readFileSync('/home/user/kashikin/data/traps.json', 'utf8')).map(t => [t.id, t]));
const MARK = ['①', '②', '③', '④'];
const F = 'Meiryo';
const FMT = { single: '単純択一', combo: '組合せ', count: '個数' };

const YEARS = [
  { kai: 14, era: '令和元年度', ad: 2019, file: '令和元年_2019_第14回.docx',
    fix: 'アップロードされた「貸金業取扱主任者2019年」では 問5⇔問6、問7⇔問8 が入れ替わっていました。正しい並びに直しています。' },
  { kai: 15, era: '令和2年度', ad: 2020, file: '令和2年_2020_第15回.docx',
    fix: 'アップロードされた「令和2年 2020年貸金問題」では、正解番号が50問中23問で公式正答と食い違っていました。公式正答に直しています。' },
  { kai: 16, era: '令和3年度', ad: 2021, file: '令和3年_2021_第16回.docx',
    fix: 'アップロードされた「令和3年2021年貸金問題」は、問題文と正解番号は公式と一致していました。' },
  { kai: 17, era: '令和4年度', ad: 2022, file: '令和4年_2022_第17回.docx',
    fix: 'アップロードされた「令和4年2022年貸金問題」には、令和4年ではなく令和3年（第16回）の問題50問が収録されていました。本ファイルは令和4年（第17回）の問題です。' },
  { kai: 18, era: '令和5年度', ad: 2023, file: '令和5年_2023_第18回.docx',
    fix: 'アップロードされた「令和5年2023年貸金問題」は、問題文と正解番号は公式と一致していました。' },
];

const t = (text, o = {}) => new TextRun({ text, font: F, size: o.size || 21, bold: o.bold, color: o.color });
const p = (text, o = {}) => new Paragraph({
  children: Array.isArray(text) ? text : [t(text, o)],
  spacing: { after: o.after ?? 90, line: o.line ?? 300 },
  indent: o.indent, alignment: o.align, heading: o.heading,
  pageBreakBefore: o.pageBreakBefore,
  border: o.rule ? { bottom: { style: BorderStyle.SINGLE, size: 6, color: '0A5A2C', space: 4 } } : undefined,
});

function tableOf(tb) {
  const w = [5400, 2200];
  const cell = (s, head, right) => new TableCell({
    width: { size: right ? w[1] : w[0], type: WidthType.DXA },
    shading: head ? { type: ShadingType.CLEAR, fill: 'E5F1E9' } : undefined,
    children: [new Paragraph({
      children: [t(s, { bold: head })],
      alignment: right ? AlignmentType.RIGHT : AlignmentType.LEFT,
      spacing: { after: 20, line: 260 },
    })],
  });
  return new Table({
    columnWidths: w,
    width: { size: w[0] + w[1], type: WidthType.DXA },
    rows: [new TableRow({ children: tb.head.map((h, i) => cell(h, true, i === 1)) })]
      .concat(tb.rows.map(r => new TableRow({ children: r.map((c, i) => cell(c, false, i === 1)) }))),
  });
}

for (const Y of YEARS) {
  const qs = DB.filter(q => q.kai === Y.kai).sort((a, b) => a.num - b.num);
  if (qs.length !== 50) throw new Error(`${Y.kai}回が${qs.length}問`);
  const body = [];

  body.push(p(`${Y.era}（${Y.ad}年）貸金業務取扱主任者資格試験`, { size: 32, bold: true }));
  body.push(p(`第${Y.kai}回　全50問`, { size: 24, color: '0A5A2C', bold: true, rule: true, after: 220 }));
  body.push(p('この文書について', { size: 22, bold: true, after: 60 }));
  body.push(p('問題文・記述ａ〜ｄ・選択肢①〜④・注記は、日本貸金業協会が公開している試験問題PDFの原文そのままです。正解は同協会の正答PDFに拠ります。', { after: 60 }));
  body.push(p(Y.fix, { after: 60 }));
  body.push(p('解説は載せていません。アップロードされた5ファイルの解説を全250問について照合したところ、設問とは別の論点を説明しているものがほとんどでした。誤った解説は学習の妨げになるため、推測で書き直すことはしていません。代わりに、出題テーマ（47分類）・条文名・選択肢どうしの対立から機械的に検出した「狙われている点」を付けています。', { after: 240 }));

  // ---- 問題編 ----
  body.push(p('問題', { size: 26, bold: true, color: '0A5A2C', rule: true, after: 180 }));
  let sec = null;
  for (const q of qs) {
    if (q.sectionShort !== sec) {
      sec = q.sectionShort;
      body.push(p(sec, { size: 23, bold: true, color: '0A5A2C', after: 120 }));
    }
    body.push(p(`【問題 ${q.num}】`, { bold: true, after: 60 }));
    body.push(p(q.stem, { after: 80 }));
    for (const [k, v] of Object.entries(q.statements)) {
      body.push(p([t(`${k}　`, { bold: true }), t(v)], { indent: { left: 340, hanging: 340 }, after: 50 }));
    }
    if (q.table) {
      body.push(p(q.table.title, { bold: true, after: 40 }));
      if (q.table.caption) body.push(p(q.table.caption, { size: 19, after: 60 }));
      body.push(tableOf(q.table));
      body.push(p('', { after: 60 }));
    }
    for (const [k, v] of Object.entries(q.options)) {
      body.push(p([t(`${k}　`, { bold: true }), t(v)], { indent: { left: 340, hanging: 340 }, after: 50 }));
    }
    if (q.note) body.push(p(q.note, { size: 19, after: 60 }));
    body.push(p('', { after: 150 }));
  }

  // ---- 解答編 ----
  body.push(p('正解と着眼点', { size: 26, bold: true, color: '0A5A2C', rule: true, after: 180, pageBreakBefore: true }));
  for (const q of qs) {
    body.push(p([t(`問題 ${q.num}　`, { bold: true }), t(`正解 ${MARK[q.answer - 1]}`, { bold: true, color: 'C6402A' })], { after: 50 }));
    body.push(p([t('分野・テーマ：', { bold: true }), t(`${q.sectionShort} ／ ${q.theme}　（${FMT[q.format]}${q.negative ? '・否定形' : ''}）`)], { size: 19, after: 40 }));
    if (q.arts && q.arts.length) {
      body.push(p([t('条文：', { bold: true }), t(q.arts.map(a => `${a.a}（${a.n}）`).join('　'))], { size: 19, after: 40 }));
    }
    if (q.traps && q.traps.length) {
      body.push(p('狙われている点', { size: 19, bold: true, after: 30 }));
      for (const id of q.traps) {
        const tp = TRAPS[id];
        if (tp) body.push(p([t(`${tp.name}：`, { bold: true }), t(tp.tip)], { size: 19, indent: { left: 240 }, after: 30 }));
      }
    }
    body.push(p('', { after: 130 }));
  }

  const doc = new Document({
    creator: '貸金業務取扱主任者 過去問1000',
    title: `${Y.era} 第${Y.kai}回 貸金業務取扱主任者資格試験`,
    styles: { default: { document: { run: { font: F, size: 21 } } } },
    sections: [{ properties: { page: { margin: { top: 1000, bottom: 1000, left: 1100, right: 1100 } } }, children: body }],
  });
  const buf = await Packer.toBuffer(doc);
  fs.writeFileSync(`/home/user/kashikin/restored/${Y.file}`, buf);
  console.log(Y.file, (buf.length / 1024).toFixed(0) + 'KB', qs.length + '問');
}
