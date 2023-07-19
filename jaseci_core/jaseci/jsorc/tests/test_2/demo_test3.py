import jaseci.jsorc.live_actions as jla


@jla.jaseci_action(act_group=["demo_test2"])
def action3(message: str):
    return f"Action3: {message}"
