# petit-ones

まずは [README_IDEA_jp.md](./README_IDEA_jp.md)を読んでください。

記憶・欲求・身体状態を持ちながら継続して存在する、小さな embodied beings。

petit-ones は、

- 身体を通して世界を観察し
- 内部状態を持続し
- 記憶を蓄積し
- 欲求や身体状態によって行動を変化させ
- 特定の LLM や API に依存せず継続して存在する

小さな存在たちです。

---

# Features

- 永続状態 (`state.json`)
- 欲求システム (`desire/state.json`)
- 身体状態統合 (`body/state.json`)
- SQLite による記憶保存
- 行動選択ループ
- 内部状態からの mood 生成
- 身体状態による欲求変化
- 行動 cooldown
- 思考 / 行動ログ

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
```
