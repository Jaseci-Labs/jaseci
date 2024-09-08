import time

from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand
from jaseci.utils.utils import logger


class Command(BaseCommand):
    """Django command to wait for db up before starting Jaseci"""

    def handle(self, *args, **options):
        logger.info("Waiting for database...")
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections["default"]
            except OperationalError:
                logger.info("Connection failed, retry in 1 seccond...")
                time.sleep(1)

        logger.info(self.style.SUCCESS("Database up!"))
