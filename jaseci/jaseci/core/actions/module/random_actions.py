import random
import faker
from datetime import datetime
from datetime import timedelta


def seed(param_list):
    """Seed random num generator"""
    random.seed(param_list[0], version=2)
    faker.Faker.seed(param_list[0])


def integer(param_list):
    """Random integeter between range"""
    return random.randint(param_list[0], param_list[1])


def sentence(param_list):
    """Get a random sentence"""
    return faker.Faker().sentence()


def time(param_list):
    """Provide a random datetime between range"""
    start = datetime.fromisoformat(param_list[0])
    end = datetime.fromisoformat(param_list[1])
    return (start + timedelta(
        seconds=random.randint(0, int((end - start).total_seconds())),
    )).isoformat()
