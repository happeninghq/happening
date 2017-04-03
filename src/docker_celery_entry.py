import os
import sys
import psycopg2
import time

DEFAULT_DATABASE_URL = "postgres://postgres:@db:5432/happening"

# This is the file that will be ran within the docker container.
print("Starting Happening celery server")

# First, we check if we're connecting to the default database
DATABASE_URL = os.environ.get('DATABASE_URL', None)
if not DATABASE_URL:
    print("A DATABASE_URL environmental variable must be provided.")
    sys.exit(1)
print("DATABASE_URL", DATABASE_URL)


def try_connection(sleep):
    """Try a connection to the database."""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        conn.close()
        return True
    except psycopg2.OperationalError as e:
        time.sleep(sleep)
        return False


sleep = 2
while not try_connection(sleep):
    print("Retrying database connection...")
    sleep *= 2

# Check redis URL
REDIS_URL = os.environ.get('REDIS_URL', None)
if not REDIS_URL:
    print("A REDIS_URL environmental variable must be provided.")
    sys.exit(1)
print("REDIS_URL", REDIS_URL)


if bool(os.environ.get('DJANGO_DEBUG', 'False') == 'True'):
    # TODO: Wrap this in autoreload
    os.system("celery -A happening worker -B -l info -Q happening")
else:
    os.system("celery -A happening worker -B -l info -Q happening")
