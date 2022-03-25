"""Built in actions for Jaseci"""
import random
# import faker
from datetime import datetime
from datetime import timedelta
from jaseci.actions.live_actions import jaseci_action


@jaseci_action()
def seed(val: int):
    """Seed random num generator"""
    random.seed(val, version=2)
    # faker.Faker.seed(param_list[0])


@jaseci_action()
def integer(start: int, end: int):
    """Random integeter between range"""
    return random.randint(start, end)


@jaseci_action()
def sentence(meta):
    """Get a random sentence"""
    fstr = ''
    for i in range(random.randint(0, 10)):
        fstr += "test "
    return fstr
    # return faker.Faker().sentence()


@jaseci_action()
def time(start_date: str, end_date: str):
    """Provide a random datetime between range"""
    start = datetime.fromisoformat(start_date)
    end = datetime.fromisoformat(end_date)
    return (start + timedelta(
        seconds=random.randint(0, int((end - start).total_seconds())),
    )).isoformat()
