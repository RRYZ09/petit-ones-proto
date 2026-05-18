# petit-ones

まずは [README_IDEA_jp.md](./README_IDEA_jp.md)を読んでください。

# 1. 整形・lint
pre-commit run --all-files

# 2. M5 CoreS3 の身体状態を読む
python -m scripts.update_m5_cores3_body --one puchiteya

# 3. 現在状態を見る
python -m scripts.inspect_one --one puchiteya

# 4. 1回だけ lifecycle を回す
python -m scripts.run_once --one puchiteya

# 5. 行動ログを見る
tail -n 3 ~/.petit_ones/characters/puchiteya/logs/actions.log

# 6. 思考ログを見る
tail -n 3 ~/.petit_ones/characters/puchiteya/logs/thoughts.log

# 7. 新しい記憶を見る
python -m scripts.inspect_memory --one puchiteya --limit 5

# 8. 旧 embodied-claude 記憶を見る
python -m scripts.inspect_legacy_memory --one puchiteya --limit 5
