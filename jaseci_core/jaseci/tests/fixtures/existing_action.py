from jaseci.actions.live_actions import jaseci_action


@jaseci_action(act_group=["sim2"])
def tester():
    return 2
