from jaseci.jsorc.live_actions import jaseci_action


@jaseci_action(act_group=["sim1"])
def tester():
    return 1
