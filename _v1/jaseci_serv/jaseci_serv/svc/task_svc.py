from json import dumps, loads
from jaseci.jsorc.jsorc import JsOrc
from jaseci.extens.svc.task_svc import TaskService as Ts
from django.db.models import Q
from django_celery_beat.models import PeriodicTask, CrontabSchedule, IntervalSchedule

#################################################
#                 TASK APP ORM                 #
#################################################


@JsOrc.service(name="task", config="TASK_CONFIG", priority=2)
class TaskService(Ts):
    ###################################################
    #                SCHEDULED QUEUING                #
    ###################################################

    def add_scheduled_queue(
        self, queue_type: object, name: str, schedule: dict, body: dict
    ):
        periodic_task = {
            "name": name,
            "task": self.get_task_name(queue_type),
            "kwargs": dumps(body),
            "one_off": schedule.get("one_off", False),
        }

        if schedule.get("type") == "interval":
            interval = {"every": 1, "period": IntervalSchedule.MINUTES}
            interval.update(schedule.get("conf", {}))
            periodic_task["interval"] = IntervalSchedule.objects.get_or_create(
                **interval
            )[0]
        else:
            crontab = {
                "minute": "*",
                "hour": "*",
                "day_of_week": "*",
                "day_of_month": "*",
                "month_of_year": "*",
            }
            crontab.update(schedule.get("conf", {}))
            periodic_task["crontab"] = CrontabSchedule.objects.get_or_create(**crontab)[
                0
            ]

        return PeriodicTask.objects.create(**periodic_task)

    def get_scheduled_queues(
        self,
        limit: int = 10,
        offset: int = 0,
        asc: bool = True,
        name: str = None,
        master=False,
    ):
        from jaseci.prim.super_master import SuperMaster

        is_admin = isinstance(master, SuperMaster)

        filter = [Q(crontab__isnull=False) | Q(interval__isnull=False), ~Q(id=1)]
        if not is_admin:
            filter.append(Q(task=self.get_task_name(self.scheduled_walker)))
        if name:
            filter.append(Q(name__icontains=name))

        pts = []
        for pt in PeriodicTask.objects.filter(*filter).order_by(
            ("" if asc else "-") + "name"
        ):
            kwargs = loads(pt.kwargs)
            mst = kwargs.get("mst")
            try:
                if is_admin or (mst != None and mst in master.jid):
                    if pt.interval:
                        schedule = {
                            "type": "interval",
                            "conf": {
                                "every": pt.interval.every,
                                "period": pt.interval.period,
                            },
                        }
                    else:
                        schedule = {
                            "type": "crontab",
                            "conf": {
                                "minute": pt.crontab.minute,
                                "hour": pt.crontab.hour,
                                "day_of_week": pt.crontab.day_of_week,
                                "day_of_month": pt.crontab.day_of_month,
                                "month_of_year": pt.crontab.month_of_year,
                            },
                        }

                    pts.append(
                        {
                            "id": pt.id,
                            "name": pt.name,
                            "schedule": schedule,
                            "kwargs": loads(pt.kwargs),
                        }
                    )
            except Exception:
                pass

        return pts[offset : offset + limit if limit else PeriodicTask.objects.count()]

    def delete_scheduled_queue(self, scheduled_queue_id: int, master):
        from jaseci.prim.super_master import SuperMaster

        is_admin = isinstance(master, SuperMaster)

        try:
            pt = PeriodicTask.objects.get(id=scheduled_queue_id)
            if pt:
                kwargs = loads(pt.kwargs)
                mst = kwargs.get("mst")
                if is_admin or (mst != None and mst in master.jid):
                    pt.delete()
                    return True
        except PeriodicTask.DoesNotExist:
            pass

        return False
