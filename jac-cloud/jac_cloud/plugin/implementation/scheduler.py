"""Jaseci Scheduler Implementations."""

from dataclasses import MISSING
from datetime import UTC, datetime
from enum import StrEnum
from logging import WARNING, getLogger
from os import getenv
from traceback import format_exception
from typing import Any, Callable

from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.util import _Undefined, undefined

from fastapi.responses import JSONResponse, ORJSONResponse

from jaclang.runtimelib.machine import JacMachineInterface as Jac

from ...core.archetype import (
    NodeAnchor,
    NodeArchetype,
    Schedule,
    ScheduleStatus,
    WalkerAnchor,
    WalkerArchetype,
)
from ...core.context import JaseciContext
from ...jaseci.datasources.localdb import MONTY_CLIENT
from ...jaseci.datasources.redis import ScheduleRedis
from ...jaseci.utils import logger, utc_datetime, utc_datetime_iso


SCHEDULER_MAX_THREAD = int(getenv("SCHEDULER_MAX_THREAD", "5"))
TASK_CONSUMER_CRON_SECOND = getenv("TASK_CONSUMER_CRON_SECOND")
TASK_CONSUMER_MULTITASK = int(getenv("TASK_CONSUMER_MULTITASK", "1"))
HAS_DB = bool(getenv("DATABASE_HOST"))


class Trigger(StrEnum):
    """Trigger Type."""

    DATE = "date"
    INTERVAL = "interval"
    CRON = "cron"


class Executor(StrEnum):
    """Executor Type."""

    THREAD = "thread"
    PROCESS = "process"


class JaseciScheduler(BackgroundScheduler):
    """Jaseci Scheduler."""

    def start(self, *args: Any, **kwargs: Any) -> None:  # noqa: ANN401
        """Override start."""
        super().start(*args, **kwargs)

        if TASK_CONSUMER_CRON_SECOND:

            @self.scheduled_job(
                trigger="cron",
                name="Task Consumer",
                second=TASK_CONSUMER_CRON_SECOND,
                max_instances=TASK_CONSUMER_MULTITASK,
            )
            def consume_task() -> None:
                """Consume Task."""
                now = utc_datetime()
                sched: dict[str, Any] | None = ScheduleRedis.lpop("scheduled")
                if sched and (
                    not sched["execute_date"] or sched["execute_date"] <= now
                ):
                    wanch = WalkerAnchor.ref(walker_id := sched["walker_id"])
                    root = NodeAnchor.ref(sched["root_id"])
                    node = (
                        NodeAnchor.ref(node_id)
                        if (node_id := sched["node_id"])
                        else root
                    )

                    if not WalkerAnchor.Collection.update_one(
                        {"_id": wanch.id, "schedule.status": "PENDING"},
                        {
                            "$set": {
                                "schedule.status": "STARTED",
                                "schedule.executed_date": now,
                            }
                        },
                    ).modified_count:
                        logger.info(f"Task `{walker_id}` skipped: {utc_datetime_iso()}")
                        if not HAS_DB:
                            MONTY_CLIENT.set(None)
                        return

                    logger.info(f"Task `{walker_id}` started: {now.isoformat()}")
                    run_task(wanch, root, node, "Task", True)
                    logger.info(f"Task `{walker_id}` done: {utc_datetime_iso()}")
                elif not HAS_DB:
                    MONTY_CLIENT.set(None)


scheduler = JaseciScheduler(
    executors={
        Executor.THREAD: ThreadPoolExecutor(SCHEDULER_MAX_THREAD),
    },
    timezone=UTC,
)

getLogger("apscheduler.executors.default").setLevel(WARNING)
getLogger("apscheduler.executors.thread").setLevel(WARNING)


def schedule_walker(
    trigger: Trigger,
    node: str | None = None,
    args: Any | None = None,
    kwargs: Any | None = None,
    misfire_grace_time: int = 1,
    coalesce: bool = True,
    max_instances: int = 1,
    next_run_time: _Undefined | Any = undefined,
    propagate: bool = False,
    save: bool = False,
    **trigger_args: Any,  # noqa: ANN401
) -> Callable:
    """Override schedule_job to trigger it once across workers and replicas."""

    def wrapper(walker: type[WalkerArchetype]) -> None:
        @scheduler.scheduled_job(
            trigger=trigger,
            args=args,
            kwargs=kwargs,
            id=walker.__name__,
            name=walker.__name__,
            misfire_grace_time=misfire_grace_time,
            coalesce=coalesce,
            max_instances=max_instances,
            next_run_time=next_run_time,
            executor="thread",
            **trigger_args,
        )
        def process(*args: Any, **kwargs: Any) -> None:  # noqa: ANN401
            now = utc_datetime()
            if propagate or ScheduleRedis.hsetnx(
                f"{walker.__name__}-{now.timestamp()}", True
            ):
                logger.info(
                    f"Scheduled Walker `{walker.__name__}` started: {now.isoformat()}"
                )
                run_task(
                    walker(*args, **kwargs).__jac__,
                    node=NodeAnchor.ref(node) if node else None,
                    save=save,
                )
                logger.info(
                    f"Scheduled Walker `{walker.__name__}` done: {utc_datetime_iso()}"
                )

            if not HAS_DB:
                MONTY_CLIENT.set(None)

    return wrapper


def remove_scheduled_walker(id: str) -> None:
    """Remove existing job."""
    scheduler.remove_job(id)


def repopulate_tasks() -> None:
    """Repopulate Tasks."""
    if TASK_CONSUMER_CRON_SECOND and (
        pendings := [
            {
                "walker_id": w.ref_id,
                "execute_date": w.schedule.execute_date,
                "node_id": w.schedule.node_id,
                "root_id": f"n::{w.root}",
            }
            for w in WalkerAnchor.Collection.find({"schedule.status": "PENDING"})
            if w.schedule
        ]
    ):
        ScheduleRedis.rpush(
            "scheduled",
            *pendings,
        )


def create_task(
    walker: WalkerArchetype, node: NodeArchetype, date: datetime | None = None
) -> str:
    """Create task."""
    root_id: str = Jac.object_ref(Jac.root())

    wanch = walker.__jac__
    wanch.schedule = Schedule(
        ScheduleStatus.PENDING, node.__jac__.ref_id, root_id, date
    )

    Jac.save(wanch)

    return wanch.ref_id


def run_task(
    walker: WalkerAnchor,
    root: NodeAnchor | None = None,
    node: NodeAnchor | None = None,
    type: str = "Task",
    save: bool = True,
) -> None:
    """Run task."""
    from ..jaseci import FastAPI

    __jac_mach__ = FastAPI.__jac_mach__  # noqa: F841

    jctx = JaseciContext.create(None, node or root)

    if root:
        jctx.root_state = root

    if walker.schedule and (root_id := walker.schedule.root_id):
        jctx.root_state = NodeAnchor.ref(root_id)
        jctx.root_state.archetype

    warch = walker.archetype

    try:
        Jac.spawn(warch, jctx.entry_node.archetype)

        resp = jctx.response(walker.returns)
        if jctx.custom is not MISSING:
            if isinstance(jctx.custom, JSONResponse):
                resp["custom"] = jctx.custom.body
            else:
                resp["custom"] = ORJSONResponse(jctx.custom).body

        resp["http_status"] = resp.pop("status")
        walker.schedule = Schedule(ScheduleStatus.COMPLETED, **resp)
    except Exception as e:
        now = utc_datetime()
        logger.exception(f"{type} `{walker.ref_id}` failed: {now.isoformat()}")
        walker.schedule = Schedule(
            ScheduleStatus.ERROR, executed_date=now, error=format_exception(e)
        )

    if save:
        Jac.save(walker)

    jctx.close()

    if not HAS_DB:
        MONTY_CLIENT.set(None)
