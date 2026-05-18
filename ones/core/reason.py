def reason_for_action(action: str, desire: dict, recent_memories: list) -> str:
    memory_count = len(recent_memories)

    if action == "observe_world":
        return f"好奇心が一番強かったので、世界を観察することにした。最近の記憶は{memory_count}件ある。"
    if action == "express_feeling":
        return f"表現したい気持ちが強くなっていたので、感じたことを表そうとした。最近の記憶は{memory_count}件ある。"
    if action == "look_for_human":
        return f"関わりたい気持ちが残っていたので、人の気配を探した。最近の記憶は{memory_count}件ある。"
    if action == "rest":
        return (
            f"休みたい気持ちが強かったので、少し休むことにした。最近の記憶は{memory_count}件ある。"
        )

    return f"大きく動かず、その場にいることにした。最近の記憶は{memory_count}件ある。"
