import os
import sys

DEFAULT_DATABASE_URL = "postgres://postgres:@db:5432/happening"

# This is the file that will be ran within the docker container.
print("Starting Happening celery server")

# First, we check if we're connecting to the default database
DATABASE_URL = os.environ.get('DATABASE_URL', None)
if not DATABASE_URL:
    print("A DATABASE_URL environmental variable must be provided.")
    sys.exit(1)
print("DATABASE_URL", DATABASE_URL)
# Check redis URL
REDIS_URL = os.environ.get('REDIS_URL', None)
if not REDIS_URL:
    print("A REDIS_URL environmental variable must be provided.")
    sys.exit(1)
print("REDIS_URL", REDIS_URL)

os.system("celery -A happening worker -B -l info -Q happening")
