# Jac Cloud Scheduler

## **Supported specs**

| **NAME**      | **TYPE**               | **DESCRIPTION**                                                                                   | **DEFAULT** |
| ------------- | ---------------------- | ------------------------------------------------------------------------------------------------- | ----------- |
| trigger       | str                    | trigger type (`cron`, `interval`, `date`)                                                         | N/A         |
| node          | str or None            | entry node if necessary, defaults to root                                                         | None        |
| args          | list[Any] or None      | list of arguments to initialize the walker                                                        | None        |
| kwargs        | dict[str, Any] or None | dict of keyword arguments to initialize the walker                                                | None        |
| max_instances | int                    | max simultaneous running job per walker type                                                      | 1           |
| next_run_time | datetime or None       | target date before the first trigger will happen                                                  | None        |
| propagate     | bool                   | if multiple jac-cloud service can trigger at the same time or first service only per trigger only | false       |
| save          | bool                   | if walker instance will be save to the db including the results                                   | false       |

## **cron** type trigger

- You need to add additional specs for cron

| **NAME**    | **TYPES**               | **DESCRIPTION**                                                | **DEFAULT** |
| ----------- | ----------------------- | -------------------------------------------------------------- | ----------- |
| year        | int or str              | 4-digit year                                                   | \*          |
| month       | int or str              | month (1-12)                                                   | \*          |
| day         | int or str              | day of month (1-31)                                            | \*          |
| week        | int or str              | ISO week (1-53)                                                | \*          |
| day_of_week | int or str              | number or name of weekday (0-6 or mon,tue,wed,thu,fri,sat,sun) | \*          |
| hour        | int or str              | hour (0-23)                                                    | \*          |
| minute      | int or str              | minute (0-59)                                                  | \*          |
| second      | int or str              | second (0-59)                                                  | \*          |
| start_date  | datetime or str or None | earliest possible date/time to trigger on (inclusive)          | None        |
| end_date    | datetime or str or None | latest possible date/time to trigger on (inclusive)            | None        |

### Example

```python
walker walker_cron {
    has arg1: int;
    has arg2: str;
    has kwarg1: int = 3;
    has kwarg2: str = "4";

    can enter with `root entry {
        print("I am a scheduled walker!")
    }

    class __specs__ {
        has private: bool = True;
        has schedule: dict = {
            "trigger": "cron",
            "args": [1, "2"],
            "kwargs": {
                "kwarg1": 30,
                "kwarg2": "40"
            },
            "save": True
        };
    }
}
```

## **interval** type trigger

- You need to add additional specs for interval

| **NAME**   | **TYPES**               | **DESCRIPTION**                             | **DEFAULT** |
| ---------- | ----------------------- | ------------------------------------------- | ----------- |
| weeks      | int                     | number of weeks to wait                     |             |
| days       | int                     | number of days to wait                      |             |
| hours      | int                     | number of hours to wait                     |             |
| minutes    | int                     | number of minutes to wait                   |             |
| seconds    | int                     | number of seconds to wait                   | 1           |
| start_date | datetime or str or None | starting point for the interval calculation |             |
| end_date   | datetime or str or None | latest possible date/time to trigger on     |             |

```python
walker walker_interval {
    has arg1: int;
    has arg2: str;
    has kwarg1: int = 3;
    has kwarg2: str = "4";

    can enter with `root entry {
        print("I am a scheduled walker!")
    }

    class __specs__ {
        has private: bool = True;
        has schedule: dict = {
            "trigger": "interval",
            "args": [1, "2"],
            "kwargs": {
                "kwarg1": 30,
                "kwarg2": "40"
            },
            "seconds": 5,
            "save": True
        };
    }
}
```

## **date** type trigger

- You need to add additional specs for interval

| **NAME** | **TYPES**       | **DESCRIPTION**                 | **DEFAULT** |
| -------- | --------------- | ------------------------------- | ----------- |
| run_date | datetime or str | the date/time to run the job at |             |

```python
walker walker_date {
    has arg1: int;
    has arg2: str;
    has kwarg1: int = 3;
    has kwarg2: str = "4";

    can enter with `root entry {
        print("I am a scheduled walker!")
    }

    class __specs__ {
        has private: bool = True;
        has schedule: dict = {
            "trigger": "date",
            "args": [1, "2"],
            "kwargs": {
                "kwarg1": 30,
                "kwarg2": "40"
            },
            "run_date": "2025-04-30T11:12:00+00:00",
            "save": True
        };
    }
}
```

# Jac Cloud Optional Task

- This will only be enabled if you have set `TASK_CONSUMER_CRON_SECOND`

## Example Use Case

```python
import from jac_cloud.plugin.implementation {create_task}

node TaskCounter {
    has val: int = 0;
}

walker get_or_create_counter {
    can enter1 with `root entry {
        tc = TaskCounter();
        here ++> tc;

        report tc;
    }

    can enter2 with TaskCounter entry {
        report here;
    }
}

walker increment_counter {
    has val: int;

    can enter with TaskCounter entry {
        here.val += self.val;
    }

    class __specs__ {
        has private: bool = True;
    }
}

walker trigger_counter_task {
    can enter with `root entry {
        tcs = [-->(`?TaskCounter)];
        if tcs {
            report create_task(increment_counter(val=1), tcs[0]);
        }
    }
}
```

- `trigger_counter_task` walker will only create walker task and will be consumed by `Task Consumer`
  - this will report walker id that can be used to retrieve it again
- task will be saved to db and also in redis
  - the polling mechanism will use redis to avoid traffic to db
    - lowest polling trigger will be 1 second. Can be set to `TASK_CONSUMER_CRON_SECOND`
  - the consume flow will be atomic and only one jac-cloud instance can process a task
- if redis is cleaned up, upon running of jac-cloud service, it will repopulate pending task to redis again
  - if ever multiple services tries to repopulate pending task to redis, since we are using atomic operations, if the task is already started it will be skipped by other services
