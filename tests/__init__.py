from ones.core.action import choose_action


def test_choose_action_curiosity():
    desire = {
        "curiosity": 0.8,
        "expression": 0.2,
        "connection": 0.1,
        "rest": 0.1,
    }

    action = choose_action(desire, {}, None)

    assert action == "observe_world"


def test_choose_action_rest():
    desire = {
        "curiosity": 0.1,
        "expression": 0.2,
        "connection": 0.1,
        "rest": 0.9,
    }

    action = choose_action(desire, {}, None)

    assert action == "rest"
