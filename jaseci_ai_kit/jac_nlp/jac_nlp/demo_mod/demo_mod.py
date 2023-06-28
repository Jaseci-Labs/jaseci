from jaseci.jsorc.live_actions import jaseci_action


@jaseci_action(act_group=["demo_mod"], allow_remote=True)
def demo_mod_action(x: int = 1, y: int = 1):
    #    print(f"x={x}, y={y}")
    return x + y


if __name__ == "__main__":
    from jaseci.jsorc.remote_actions import launch_server

    launch_server(port=8000)
