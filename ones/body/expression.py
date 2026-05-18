from urllib.error import HTTPError, URLError

from ones.body.m5_cores3_body import blink, set_face


def express_action(one_id: str, body: dict, action: str) -> list[str]:
    if body.get("body_type") != "m5_cores3":
        return []

    try:
        if action == "rest":
            blink(one_id, left=True, right=True)
            return ["rest を表情に反映した"]

        if action == "observe_world":
            set_face(one_id, eye_x=20, eye_y=0, mouth=0)
            return ["observe_world を表情に反映した"]

        if action == "look_for_human":
            set_face(one_id, eye_x=-35, eye_y=0, mouth=0)
            return ["look_for_human を表情に反映した"]

        if action == "express_feeling":
            set_face(one_id, eye_x=0, eye_y=-10, mouth=60)
            return ["express_feeling を表情に反映した"]

    except (URLError, HTTPError, TimeoutError, OSError) as exc:
        return [f"表情反映に失敗した: {exc}"]

    return []
