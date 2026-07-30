# デザインシステム

学習アプリ（`app/template.html`）で実際に使っているトークンとコンポーネントを、
Claude Design（claude.ai/design）の Design System ペインにそのまま載せられる形で切り出したものです。

`design/index.html` をブラウザで開けば、接続しなくても同じ単位で見られます。

## 中身

| カード | ファイル | 内容 |
|---|---|---|
| **Foundations** | | |
| 配色 | `foundations/color.html` | 深緑・朱・紺・紫の4色、意味、4分野への割り当て、地と文字の階調 |
| 文字 | `foundations/type.html` | メイリオ1本のスケールと、長文設問の組み方 |
| 形と密度 | `foundations/shape.html` | 角丸2段階・影なし・一覧の行の詰め方 |
| **Components** | | |
| ヘッダーバー | `components/header.html` | ホーム／演習中／模試の3状態 |
| ボタン | `components/buttons.html` | 主動線・下部バー・解答後の枝分かれ・出題条件 |
| タグ | `components/tags.html` | 分野・出題形式・否定形・頻出・診断の種別 |
| 一覧の行 | `components/list-rows.html` | 分野別・テーマ47件・解答履歴 |
| 設問 | `components/question.html` | 解答前・解答後・引っかけの提示 |
| 記述カード | `components/statements.html` | ａ〜ｄに○×を付ける（個数・組合せ問題） |
| 弱点診断 | `components/diagnosis.html` | 引っかけの型・テーマ・読み方の5軸 |
| 進み具合 | `components/progress.html` | 段位・連続日数・合格可能性・到達度・実績 |
| 状態 | `components/empty-state.html` | 初回起動・目標達成・復習が溜まったとき |

各ファイルの1行目に `<!-- @dsCard group="…" name="…" subtitle="…" -->` を置いてあります。
Claude Design はこの印からペインのカード一覧を組むので、別途の登録は要りません。

## トークンは二重管理していない

各カードの `:root` は `app/template.html` の `<style>` から機械的に写しています。
アプリ側の色を変えれば、再生成でこちらも追従します。手で書き写した箇所はありません。

```bash
python3 tools/design/01_foundations.py   # 配色・文字・形
python3 tools/design/02_chrome.py        # ヘッダー・ボタン・タグ
python3 tools/design/03_content.py       # 一覧・設問・記述カード
python3 tools/design/04_state.py         # 診断・進み具合・状態
python3 tools/design/05_viewer.py        # design/index.html
```

## Claude Design へ載せる

`DesignSync` は claude.ai/design の認可が要ります。Claude Code on the web からは
`/design-login` が使えない（対話端末が必要）ため、次のどちらかで繋ぎます。

1. **Claude Design 側から「Send to Claude Code Web」** — プロジェクトがワークスペースに入るので、
   そのまま `design/` を push できます。
2. **ローカルの Claude Code から** `/design-login` を通してこのリポジトリを開く。

繋がったあとの手順は次のとおりです。

```
DesignSync list_projects                     # 書き込めるデザインシステムを探す
DesignSync create_project  name="貸金業務取扱主任者"   # 無ければ作る
DesignSync finalize_plan   projectId=<uuid>
                           localDir=/path/to/kashikin/design
                           writes=["foundations/*.html","components/*.html","README.md"]
DesignSync write_files     planId=<id>  files=[{path:"foundations/color.html",
                                                localPath:"foundations/color.html"}, …]
```

`finalize_plan` で書き込むパスを固定してから `write_files` に進む順序が決まっており、
計画外のパスへの書き込みは弾かれます。差し替えは1コンポーネントずつ行い、
まとめて置き換えることはしません。
