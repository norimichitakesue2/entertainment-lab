# Entertainment Lab

ゲームプランナー Norimichi Takesue の個人サイト。ソーダスプリント（開発中）の紹介と、ソーシャルゲーム他メディアの構造分析（エンタメ設計研究所）を掲載。

## 公開URL

GitHub Pages: https://norimichitakesue2.github.io/entertainment-lab/

- `/` — トップページ（ソーダスプリント／制作思想／研究所紹介／自己紹介）
- `/lab.html` — エンタメ設計研究所

両ページ上部の「ホーム ⇄ 研究所」タブで行き来できる。

## ファイル構成

- `index.html` — トップページ。CSS・JSは1ファイル完結（研究所とは独立）
- `assets/` — トップページの素材（`soda-cover.jpg` ポスター画像、`soda-gameplay.mp4` プレイ動画）
- `lab.html` — 研究所の公開中最新ビルド（中身は `entertainment_lab_v{N}.html` の最新と同一）
- `entertainment_lab_v{N}.html` — 研究所のバージョン履歴。Cowork の週次タスクが新版を生成し、`lab.html` にコピーして commit/push する
- `bump.sh` — 最新の `entertainment_lab_v{N}.html` を `lab.html` にコピーするヘルパー
- `notes.md` — 一次観察メモ（`.gitignore` で除外、ローカル限定）

## 研究所の更新フロー

1. 新しい `entertainment_lab_v{N+1}.html` を作る（週次タスク or 作品追加）
2. `./bump.sh` で `lab.html` に同期
3. `git add . && git commit -m "..." && git push`
4. GitHub Pages が自動デプロイ

**注意：** 研究所の内容を `index.html` にコピーしないこと（トップページが上書きされる）。研究所HTML冒頭の `<nav class="site-tabs">` は残す。
