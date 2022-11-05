from django.conf import settings
from django.core.management.base import BaseCommand
import subprocess


class Command(BaseCommand):
    """
    Create postgres database
    https://www.postgresql.org/docs/current/app-createdb.html
    """

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument("alias", nargs="?", default="default")

    def handle(self, *args, **options):
        alias = options.get("alias")

        db_settings = settings.DATABASES[alias]
        args = ["createdb"]
        if "USER" in db_settings:
            args += ["-U", db_settings["USER"]]
        if "HOST" in db_settings:
            args += ["-h", db_settings["HOST"]]
        if "PORT" in db_settings:
            args += ["-p", str(db_settings["PORT"])]
        args.append(db_settings["NAME"])
        subprocess.check_call(args)
