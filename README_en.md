# petit-ones

Persistent embodied beings with memory, desire, and body-state driven behavior.

petit-ones are small embodied systems that:

- observe the world through a body
- maintain persistent internal state
- accumulate memories
- change behavior based on desire and body conditions
- continue existing independently from specific LLM vendors or APIs

---

# Features

- Persistent state (`state.json`)
- Desire system (`desire/state.json`)
- Body state integration (`body/state.json`)
- SQLite memory storage
- Action selection loop
- Mood generation from internal state
- Body-driven desire changes
- Action cooldown system
- Thought / action logging

---

# Current Architecture

```text
body
↓
desire
↓
action selection
↓
memory
↓
next action

Repository Structure
petit-ones/
├── ones/
│   ├── memory/
│   │   ├── schema.sql
│   │   └── sqlite_memory.py
│   └── storage/
│       └── paths.py
│
├── scripts/
│   ├── inspect_one.py
│   ├── inspect_memory.py
│   ├── run_once.py
│   └── update_mock_body.py
│
└── ~/.petit_ones/
    └── characters/
        └── puchiteya/
            ├── SOUL.md
            ├── state.json
            ├── memory.sqlite3
            ├── body/
            │   └── state.json
            ├── desire/
            │   └── state.json
            └── logs/
                ├── actions.log
                └── thoughts.log
Requirements
Python 3.11+
sqlite3
Setup

ランタイムデータディレクトリ作成:

mkdir -p ~/.petit_ones/characters/puchiteya/{body,desire,logs}

データベース作成:

sqlite3 ~/.petit_ones/characters/puchiteya/memory.sqlite3 ".databases"
Initialize Files
state.json
{
  "one_id": "puchiteya",
  "status": "awake",
  "mood": "neutral",
  "last_action": null,
  "updated_at": null
}
desire/state.json
{
  "curiosity": 0.45,
  "expression": 0.35,
  "connection": 0.30,
  "rest": 0.20,
  "updated_at": null
}
body/state.json
{
  "body_type": "mock",
  "location": "unknown",
  "battery": null,
  "temperature": null,
  "human_nearby": false,
  "sensor_summary": "まだ身体からの入力はありません",
  "updated_at": null
}
Run

mock body 更新:

python scripts/update_mock_body.py --one puchiteya

1回分の lifecycle 実行:

python scripts/run_once.py --one puchiteya

現在状態確認:

python scripts/inspect_one.py --one puchiteya

記憶確認:

python scripts/inspect_memory.py --one puchiteya
Current Behavior

現在 run_once.py は:

身体状態を読む
身体状態を欲求へ反映
最近の記憶を読む
次の行動を選択
行動後の欲求変化
mood 生成
ログ保存
記憶保存

を行います。

Body → Desire Effects

例:

温度が高い → rest 上昇
人が近い → connection 上昇
周囲の変化 → curiosity 上昇
バッテリー低下 → rest 上昇
Desire → Action Mapping
Desire	Action
curiosity	observe_world
expression	express_feeling
connection	look_for_human
rest	rest
Logs
actions.log

保存内容:

選択行動
身体状態
欲求状態
body effects
thoughts.log

保存内容:

行動理由
最近の記憶
mood
body effects
Memory

SQLite schema:

CREATE TABLE memories (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  one_id TEXT NOT NULL,
  created_at TEXT NOT NULL,
  kind TEXT NOT NULL,
  content TEXT NOT NULL,
  source TEXT
);
Future Work
ローカル LLM 統合
実ロボット身体接続
persistent runtime loop
時間帯 lifecycle
習慣システム
関係性記憶
MCP replacement runtime
自律スケジューリング
複数 one 間 interaction
Notes

現在の実装では、

desire system
mood generation
action selection

を intentionally LLM 外で保持しています。

LLM は現在:

解釈
言語生成
内省

用途を想定しており、

persistent state transition の中心には置いていません。
