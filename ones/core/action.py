def choose_action(
    desire: dict,
    body: dict,
    last_action: str | None = None,
) -> str:
    scores = {k: v for k, v in desire.items() if isinstance(v, (int, float))}

    if not scores:
        return "stay_still"

    action_map = {
        "curiosity": "observe_world",
        "expression": "express_feeling",
        "connection": "look_for_human",
        "rest": "rest",
    }

    action_scores = {action_map[k]: v for k, v in scores.items() if k in action_map}

    if last_action in action_scores:
        action_scores[last_action] *= 0.7

    return max(action_scores, key=action_scores.get)
