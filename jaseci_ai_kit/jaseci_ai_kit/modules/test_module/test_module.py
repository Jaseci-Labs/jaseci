from jaseci.actions.live_actions import jaseci_action


@jaseci_action(act_group=["test_module"], allow_remote=True)
def call(a: str):
    return f"test module received {a}."


if __name__ == "__main__":
    from jaseci.actions.remote_actions import launch_server

    launch_server(port=8000)
