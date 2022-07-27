from jaseci.actions.live_actions import jaseci_action


@jaseci_action(act_group=["yolov5"], allow_remote=True)
def detect(files_list: int):

    return ""


if __name__ == "__main__":
    from jaseci.actions.remote_actions import launch_server

    launch_server(port=8000)
