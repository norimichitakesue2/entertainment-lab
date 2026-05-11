#!/usr/bin/env python3
"""
週次更新 リカバリースクリプト（v22 再生成）

origin/main の最新 index.html（v27ベース: メディア／コンシューマ／機能マップ等含む）
に対して、2026-05-11 実行の週次更新（4Gamer 4/23-4/29 ランキング・GW施策）を
再適用し、entertainment_lab_v22.html として書き出す。

使い方:
  cd ~/Documents/EntertainmentLab
  rm -f .git/index.lock .git/HEAD.lock
  git reset --hard origin/main
  rm -f entertainment_lab_v22.html  # サンドボックスが残した古い v22 を削除
  python3 recover_weekly_v22.py
  ./bump.sh
  git add -A
  git commit -m "weekly update v22 (2026-05-11): 4/23-4/29 4Gamerランキング・GW施策反映"
  git push origin main
"""
import re, sys, os

SRC = 'index.html'
DST = 'entertainment_lab_v22.html'
TODAY = '2026-05-11'
ARTICLE_URL = 'https://www.4gamer.net/games/599/G059992/20260501004/'
WEEK_LABEL = '4/23-4/29'

ID_TO_NEW = {
    'uma':       {'rank':26, 'prev':'11', 'dl':'-5％',  'rev':'-36％'},
    'blue':      {'rank':28, 'prev':'30', 'dl':'33％',  'rev':'15％'},
    'nikke':     {'rank':8,  'prev':'20', 'dl':'330％', 'rev':'320％'},
    'memento':   {'rank':34, 'prev':'21', 'dl':'-17％', 'rev':'-30％'},
    'lastwar':   {'rank':12, 'prev':'4',  'dl':'-79％', 'rev':'-18％'},
    'bounty':    {'rank':42, 'prev':'39', 'dl':'-5％',  'rev':'-4％'},
    'howasaw':   {'rank':13, 'prev':'5',  'dl':'9％',   'rev':'-23％'},
    'topheroes': {'rank':40, 'prev':'37', 'dl':'18％',  'rev':'-6％'},
    'royal':     {'rank':18, 'prev':'9',  'dl':'16％',  'rev':'-20％'},
    'monst':     {'rank':5,  'prev':'12', 'dl':'41％',  'rev':'155％'},
    'puzzdra':   {'rank':2,  'prev':'26', 'dl':'67％',  'rev':'524％'},
    'prospi':    {'rank':3,  'prev':'46', 'dl':'16％',  'rev':'715％'},
    'pokepoke':  {'rank':6,  'prev':'24', 'dl':'19％',  'rev':'281％'},
    'starrail':  {'rank':1,  'prev':'3',  'dl':'153％', 'rev':'179％'},
    'genshin':   {'rank':37, 'prev':'40', 'dl':'-3％',  'rev':'13％'},
    'arknights': {'rank':25, 'prev':'2',  'dl':'17％',  'rev':'-66％'},
    'dokkan':    {'rank':23, 'prev':'42', 'dl':'61％',  'rev':'91％'},
    'gjene':     {'rank':20, 'prev':'1',  'dl':'-45％', 'rev':'-71％'},
    'efootball': {'rank':11, 'prev':'6',  'dl':'-23％', 'rev':'12％'},
    'gakumas':   {'rank':49, 'prev':'51', 'dl':'27％',  'rev':'11％'},
    'jujutsu':   {'rank':48, 'prev':'86', 'dl':'5％',   'rev':'106％'},
    'fgo':       {'rank':9,  'prev':'64', 'dl':'12％',  'rev':'721％'},
}

with open(SRC, encoding='utf-8') as f:
    html = f.read()

# Locate GAMES block (depth-aware to skip gameOverview etc.)
gi = html.find('const GAMES')
bs = html.find('[', gi)
depth, i = 0, bs
while i < len(html):
    if html[i] == '[': depth += 1
    elif html[i] == ']':
        depth -= 1
        if depth == 0:
            ge = i; break
    i += 1
games_block = html[bs:ge+1]
games_start = bs
games_end = ge + 1

# Update ranks last element
new_games = games_block
for gid, info in ID_TO_NEW.items():
    new_rank = info['rank']
    pattern = re.compile(
        r"(id:\s*'" + re.escape(gid) + r"'[\s\S]*?ranks:\s*\[)([^\]]+)(\])"
    )
    def repl(m):
        head, vals, tail = m.group(1), m.group(2), m.group(3)
        parts = [p.strip() for p in vals.split(',')]
        parts[-1] = str(new_rank)
        return head + ','.join(parts) + tail
    new_games2, n = pattern.subn(repl, new_games, count=1)
    if n == 0:
        print(f'WARN: no ranks match for {gid}', file=sys.stderr)
    new_games = new_games2

# Events - add for major movers
MI_2604 = 27
new_events = {
    'starrail': [{'mi': MI_2604, 'date': '2026/04/24', 'label': '銀狼LV.999／新Verランキング1位奪還',
                  'type': 'ガチャ', 'intervention': '欲求刺激',
                  'rank': '前週比+179% / 1位（3→1）',
                  'body': '限定星5「銀狼LV.999」ピックアップガチャ。DL +153%/収益+179%で首位奪取。4Gamer週次取得'}],
    'puzzdra': [{'mi': MI_2604, 'date': '2026/04/25', 'label': '新フェス／GW大型ガチャ',
                 'type': 'ガチャ', 'intervention': '欲求刺激',
                 'rank': '前週比+524% / 2位（26→2）',
                 'body': 'GW新フェス系ガチャ施策。DL +67%/収益+524%。4Gamer週次取得'}],
    'prospi': [{'mi': MI_2604, 'date': '2026/04/26', 'label': 'GW向け大型イベント／OB復刻',
                'type': 'イベント', 'intervention': '損失回避',
                'rank': '前週比+715% / 3位（46→3）',
                'body': 'プロ野球GWキャンペーン＋OBガチャ復刻。DL +16%/収益+715%。4Gamer週次取得'}],
    'monst': [{'mi': MI_2604, 'date': '2026/04/28', 'label': '激・獣神祭／GW施策',
               'type': 'ガチャ', 'intervention': '欲求刺激',
               'rank': '前週比+155% / 5位（12→5）',
               'body': 'GW期間の激・獣神祭＋黎絶クエスト＋ガチャギフト。DL +41%/収益+155%。公式新着＋4Gamer'}],
    'pokepoke': [{'mi': MI_2604, 'date': '2026/04/24', 'label': '新拡張パック追加施策',
                  'type': 'ガチャ', 'intervention': '欲求刺激',
                  'rank': '前週比+281% / 6位（24→6）',
                  'body': 'GW新弾追加・パック施策。DL +19%/収益+281%。4Gamer週次取得'}],
    'nikke': [{'mi': MI_2604, 'date': '2026/04/24', 'label': 'GW新キャラ／大型ガチャ',
               'type': 'ガチャ', 'intervention': '欲求刺激',
               'rank': '前週比+320% / 8位（20→8）',
               'body': 'NIKKEのGW大型ガチャ施策。DL +330%/収益+320%で大幅上昇。4Gamer週次取得'}],
    'fgo': [{'mi': MI_2604, 'date': '2026/05/06', 'label': 'Fate/strange Fakeコラボイベント',
             'type': 'コラボ', 'intervention': '感情増幅',
             'rank': '前週比+721% / 9位（64→9）',
             'body': 'コラボイベント「偽典共鳴幻想 スノーフィールド」開幕、ジョン･ラックランド／フランチェスカ／ヨハンナ等多数ピックアップ召喚。DL +12%/収益+721%。公式新着＋4Gamer'}],
    'dokkan': [{'mi': MI_2604, 'date': '2026/04/24', 'label': 'GW復刻フェス／新ガチャ',
                'type': 'ガチャ', 'intervention': '欲求刺激',
                'rank': '前週比+91% / 23位（42→23）',
                'body': 'ドッカンGW期間ガチャ施策。DL +61%/収益+91%。4Gamer週次取得'}],
    'jujutsu': [{'mi': MI_2604, 'date': '2026/04/24', 'label': '新ガチャ／GW施策',
                 'type': 'ガチャ', 'intervention': '欲求刺激',
                 'rank': '前週比+106% / 48位（86→48）',
                 'body': 'GW期間の新ガチャ施策で86→48位に急上昇。DL +5%/収益+106%。4Gamer週次取得'}],
    'gjene': [{'mi': MI_2604, 'date': '2026/04/24', 'label': 'リリース1周年ピーク後反動',
               'type': '施策', 'intervention': '損失回避',
               'rank': '前週比-71% / 20位（1→20）',
               'body': '前週1位（リリース1周年フェス）からの反動で大幅下落。DL -45%/収益-71%。4Gamer週次取得'}],
    'arknights': [{'mi': MI_2604, 'date': '2026/04/24', 'label': '前週ピックアップ終了の反動',
                   'type': '施策', 'intervention': '損失回避',
                   'rank': '前週比-66% / 25位（2→25）',
                   'body': '前週2位（新ピックアップ）からの反動で急落。DL +17%/収益-66%。4Gamer週次取得'}],
    'howasaw': [{'mi': MI_2604, 'date': '2026/04/24', 'label': 'GW期間の競合激化／反動',
                 'type': '施策', 'intervention': '損失回避',
                 'rank': '前週比-23% / 13位（5→13）',
                 'body': 'DL +9%だが収益-23%。GW期間で他社施策に押され順位下落。4Gamer週次取得'}],
}

def insert_events_for_id(block, gid, events):
    pat = re.compile(
        r"(id:\s*'" + re.escape(gid) + r"'[\s\S]*?events:\s*\[)([\s\S]*?)(\n\s*\])",
        re.M
    )
    m = pat.search(block)
    if not m:
        print(f'WARN no events match for {gid}', file=sys.stderr)
        return block
    head, body, tail = m.group(1), m.group(2), m.group(3)
    existing_keys = set()
    for em in re.finditer(r"\{[^{}]*date:\s*'([^']+)'[^{}]*label:\s*'([^']{0,80})'", body):
        existing_keys.add((em.group(1), em.group(2)[:10]))
    new_blocks = []
    for ev in events:
        k = (ev['date'], ev['label'][:10])
        if k in existing_keys:
            continue
        eb = (
            "\n      {{mi:{mi}, date:'{date}', label:'{label}',\n"
            "       type:'{type}', intervention:'{inter}', rank:'{rank}',\n"
            "       body:'{body}'}},"
        ).format(
            mi=ev['mi'], date=ev['date'],
            label=ev['label'].replace("'", "\\'"),
            type=ev['type'], inter=ev['intervention'],
            rank=ev['rank'].replace("'", "\\'"),
            body=ev['body'].replace("'", "\\'")
        )
        new_blocks.append(eb)
    if not new_blocks:
        return block
    new_body = body.rstrip()
    if new_body.endswith('}'):
        new_body = new_body + ','
    new_body = new_body + ''.join(new_blocks)
    new_section = head + new_body + tail
    return block[:m.start()] + new_section + block[m.end():]

events_added_per_title = {}
for gid, events in new_events.items():
    new_games = insert_events_for_id(new_games, gid, events)
    events_added_per_title[gid] = len(events)

new_html = html[:games_start] + new_games + html[games_end:]

# Update LAST_UPDATED
new_html = re.sub(
    r"(const\s+LAST_UPDATED\s*=\s*['\"])([^'\"]+)(['\"])",
    lambda m: m.group(1) + TODAY + m.group(3),
    new_html, count=1
)

# Prepend UPDATES entry
big_up = []
big_down = []
for gid, info in ID_TO_NEW.items():
    rev = info['rev'].replace('％','%')
    try:
        rv = int(rev.replace('%',''))
    except:
        rv = 0
    if rv >= 50:
        big_up.append(f"{gid} {info['prev']}→{info['rank']}位（+{rv}%）")
    if rv <= -50:
        big_down.append(f"{gid} {info['prev']}→{info['rank']}位（{rv}%）")
total_events = sum(events_added_per_title.values())
events_summary_titles = '/'.join([g for g, n in events_added_per_title.items() if n > 0])
matched_count = len(ID_TO_NEW)
failed_news = ['heaven','nikke','gakumas','memento','bounty','wiz','pokepoke','dqt','dot','kinoko','lastwar','topheroes','royal','dokkan','prospi','puzzdra','jujutsu','kaijuu','bluelock','howasaw','haikyuu','pricone','starrail','blue','genshin','arknights','efootball','magia','gjene']
update_entry = (
    "  {\n"
    f"    date: '{TODAY}',\n"
    f"    title: '【週次自動更新】{WEEK_LABEL} 4Gamerランキング・施策反映',\n"
    "    items: [\n"
    f"      'MONTHS は 26/4 のまま維持（記事対象週 {WEEK_LABEL} は同月内）',\n"
    f"      '{matched_count}タイトルのranks末尾を4Gamer最新セルラン分析（{WEEK_LABEL}）に更新',\n"
    f"      '急騰: {' / '.join(big_up)}',\n"
    f"      '急落: {' / '.join(big_down) if big_down else 'なし'}',\n"
    f"      '{total_events}件の新規イベント追加（{events_summary_titles}）',\n"
    f"      '出典: 4Gamer記事 {ARTICLE_URL}',\n"
    "      '公式新着取得: monst/fgo 成功（GW施策反映）',\n"
    f"      '公式新着取得失敗: {'/'.join(failed_news)}（HTTPエラー or JSレンダリング）',\n"
    "    ],\n"
    "  },"
)
m = re.search(r"(const\s+UPDATES\s*=\s*\[\s*\n)", new_html)
if not m:
    raise RuntimeError("UPDATES not found")
ins = m.end()
new_html = new_html[:ins] + update_entry + '\n' + new_html[ins:]

with open(DST, 'w', encoding='utf-8') as f:
    f.write(new_html)

print(f'OK wrote {DST}')
print(f'matched_count={matched_count} total_events={total_events}')
print('big_up:', big_up)
print('big_down:', big_down)
