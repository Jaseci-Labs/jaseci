from jaseci.jsorc.live_actions import jaseci_action


@jaseci_action(act_group=["example_module"], allow_remote=True)
def call(a: str):
    return f"example module received {a}."


if __name__ == "__main__":
    from jaseci.jsorc.remote_actions import launch_server

    launch_server(port=8000)
