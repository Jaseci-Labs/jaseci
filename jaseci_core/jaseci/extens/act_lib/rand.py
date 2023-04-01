"""Built in actions for Jaseci"""
import random

# import faker
from datetime import datetime
from datetime import timedelta
from jaseci.jsorc.live_actions import jaseci_action

lorem_words = (
    "adipisci aliquam amet consectetur dolor dolore dolorem eius "
    "est et incidunt ipsum labore magnam modi neque non numquam "
    "porro quaerat qui quia quisquam sed sit tempora ut velit "
    "voluptatem"
).split()


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
def choice(lst: list):
    """Random select and return item in list"""
    return random.choice(lst)


@jaseci_action()
def uniform(low: float, high: float):
    """Random select a float between low an high"""
    return random.uniform(low, high)


@jaseci_action()
def sentence(min_lenth: int = 4, max_length: int = 10, sep: str = " "):
    """Get a random sentence"""
    n = random.randint(min_lenth, max_length)
    s = sep.join(word() for _ in range(n))
    return s[0].upper() + s[1:] + "."


@jaseci_action()
def paragraph(min_lenth: int = 4, max_length: int = 8, sep: str = " "):
    """Get a random paragraph"""
    n = random.randint(min_lenth, max_length)
    p = sep.join(sentence() for _ in range(n))
    return p


@jaseci_action()
def text(min_lenth: int = 3, max_length: int = 6, sep: str = "\n\n"):
    """Get a random text"""
    n = random.randint(min_lenth, max_length)
    t = sep.join(paragraph() for _ in range(n))
    return t


@jaseci_action()
def word():
    """Get a random sentence"""
    return random.choice(lorem_words)


@jaseci_action()
def time(start_date: str, end_date: str):
    """Provide a random datetime between range"""
    start = datetime.fromisoformat(start_date)
    end = datetime.fromisoformat(end_date)
    return (
        start
        + timedelta(
            seconds=random.randint(0, int((end - start).total_seconds())),
        )
    ).isoformat()
