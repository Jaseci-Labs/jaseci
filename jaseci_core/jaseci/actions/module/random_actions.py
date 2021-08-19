import random
# import faker
from datetime import datetime
from datetime import timedelta


def seed(param_list, meta):
    """Seed random num generator"""
    random.seed(param_list[0], version=2)
    # faker.Faker.seed(param_list[0])


def integer(param_list, meta):
    """Random integeter between range"""
    return random.randint(param_list[0], param_list[1])


def sentence(param_list, meta):
    """Get a random sentence"""
    fstr = ''
    for i in range(random.randint(0, 10)):
        fstr += "test "
    return fstr
    # return faker.Faker().sentence()


def time(param_list, meta):
    """Provide a random datetime between range"""
    start = datetime.fromisoformat(param_list[0])
    end = datetime.fromisoformat(param_list[1])
    return (start + timedelta(
        seconds=random.randint(0, int((end - start).total_seconds())),
    )).isoformat()
