def memory_text_for_action(one_id: str, action: str) -> str:
    if action == "observe_world":
        return f"{one_id}は世界を観察した。"
    if action == "express_feeling":
        return f"{one_id}は感じたことを表そうとした。"
    if action == "look_for_human":
        return f"{one_id}は人の気配を探した。"
    if action == "rest":
        return f"{one_id}は少し休んだ。"

    return f"{one_id}はその場にいた。"
