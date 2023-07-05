from jaseci.jsorc.live_actions import jaseci_action
import time
import random


@jaseci_action(act_group=["demo_mod"], allow_remote=True)
def demo_mod_action(x: int = 1, y: int = 1):
    # Generate a random sleep time between 1 and 3 seconds
    sleep_time = random.uniform(1, 3)
    # Sleep for the generated time
    time.sleep(sleep_time)
    return x + y


if __name__ == "__main__":
    from jaseci.jsorc.remote_actions import launch_server

    launch_server(port=8000)
