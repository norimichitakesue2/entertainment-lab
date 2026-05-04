# Entertainment Lab

ソーシャルゲーム他メディアのセルラン推移と施策を観察するための個人サイト。

## 公開URL

GitHub Pages にデプロイ済み。`index.html` がエントリ。

## ファイル構成

- `index.html` — 公開中の最新ビルド（中身は `entertainment_lab_v{N}.html` の最新と同一）
- `entertainment_lab_v{N}.html` — バージョン履歴。Cowork の週次タスクが新版を生成し、`index.html` にコピーして commit/push する流れ
- `bump.sh` — 最新の `entertainment_lab_v{N}.html` を `index.html` にコピーするヘルパー
- `notes.md` — 一次観察メモ（`.gitignore` で除外、ローカル限定）

## 週次更新フロー

1. Cowork のスケジュールタスクが `entertainment_lab_v{N+1}.html` を生成
2. `./bump.sh` で `index.html` に同期
3. `git add . && git commit -m "weekly update v{N+1}" && git push`
4. GitHub Pages が自動デプロイ
