#!/usr/bin/env bash
# 週次更新 v22 リカバリースクリプト
#
# 状況: 2026-05-11 の週次自動実行で v22 を作成・コミットしたが、
# リモート main がローカルより先行（v22-v27 = メディア/コンシューマ/機能マップ等の
# 手動更新 6 commits）していたため push がリジェクトされた。
# また、サンドボックスのFUSEマウントが .git/index.lock を残し、
# 自動再リカバリーができない状態。
#
# このスクリプトは:
#   1. 残った lockfile を削除
#   2. ローカルを origin/main に reset --hard（先行のv22-v27を全部取り込む）
#   3. 残骸の entertainment_lab_v22.html を削除
#   4. リモート最新の index.html に対して週次更新を再適用
#   5. bump.sh → git add → commit → push
set -e
cd "$(dirname "$0")"

echo "[1/7] removing stale git lockfiles..."
rm -f .git/index.lock .git/HEAD.lock

echo "[2/7] fetching origin/main..."
git fetch origin main

echo "[3/7] resetting local main to origin/main (drops local v22 commit)..."
git reset --hard origin/main

echo "[4/7] removing stale entertainment_lab_v22.html (if any from sandbox)..."
rm -f entertainment_lab_v22.html

echo "[5/7] applying weekly update to latest index.html..."
python3 recover_weekly_v22.py

echo "[6/7] running bump.sh..."
./bump.sh

echo "[7/7] git commit & push..."
git add -A
git commit -m "weekly update v22 (2026-05-11): 4/23-4/29 4Gamerランキング・GW施策反映"
git push origin main

echo ""
echo "✅ 完了! GitHub Pages は1-2分で更新されます。"
echo "   https://norimichitakesue2.github.io/entertainment-lab/"
