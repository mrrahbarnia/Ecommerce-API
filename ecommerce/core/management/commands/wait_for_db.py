"""
Custom command for waiting for db to run successfully.
"""
# import time

# from psycopg2 import OperationalError as Psycopg2Error

# from django.db.utils import OperationalError
# from django.core.management.base import BaseCommand


# class Command(BaseCommand):
#     """Custom command for waiting for db until it's ready."""

#     def handle(self, *args, **options):
#         """Entrypoint for command."""

#         self.stdout.write("Waiting for database...")
#         db_status = False
#         while db_status is False:
#             try:
#                 self.check(databases=['default'])
#                 db_status = True
#             except (Psycopg2Error, OperationalError):
#                 self.stdout.write(
#                     'Database is unavailable,wait for 1 second...'
#                 )
#                 time.sleep(1)
#         self.stdout.write(self.style.SUCCESS(
#             'Database is available!'
#         ))
