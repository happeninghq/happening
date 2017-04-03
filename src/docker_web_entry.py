import os
import sys
import psycopg2
import time
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

DEFAULT_DATABASE_URL = "postgres://postgres:@db:5432/happening"

# This is the file that will be ran within the docker container.
print("Starting Happening web server")

# First, we check if we're connecting to the default database
DATABASE_URL = os.environ.get('DATABASE_URL', None)
if not DATABASE_URL:
    print("A DATABASE_URL environmental variable must be provided.")
    sys.exit(1)
print("DATABASE_URL", DATABASE_URL)


def get_database_connection(url, tries=3):
    """Attempt to connect to the database, looping if needed."""
    try:
        conn = psycopg2.connect(url)
        conn.close()
    except psycopg2.OperationalError as e:
        if ('could not connect to server' in str(e)):
            if tries <= 0:
                raise e
            else:
                print("Waiting for database...")
                time.sleep(5)
                get_database_connection(url, tries - 1)
        elif ('database "happening" does not exist' in str(e) and
                url == DEFAULT_DATABASE_URL):
            # We're using the default database and the database doesn't exist
            print("The database doesn't exist. Creating it.")
            conn = psycopg2.connect("postgres://postgres:@db:5432/")
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cur = conn.cursor()
            cur.execute('CREATE DATABASE happening')
            cur.close()
            conn.close()

            os.system("./manage.py migrate")
            os.system("./manage.py loaddata fixtures/common fixtures/users")
        else:
            raise e
    except Exception as e:
        print("There was a database error.")
        raise e


get_database_connection(DATABASE_URL)

# Running required migrations
os.system("./manage.py migrate")


# Check redis URL
REDIS_URL = os.environ.get('REDIS_URL', None)
if not REDIS_URL:
    print("A REDIS_URL environmental variable must be provided.")
    sys.exit(1)
print("REDIS_URL", REDIS_URL)

# Run using gunicorn
if bool(os.environ.get('DJANGO_DEBUG', 'False') == 'True'):
    os.system("python manage.py runserver 0.0.0.0:8000")
else:
    os.system("gunicorn happening.wsgi --bind 0.0.0.0:8000 " +
              " --log-file - --timeout 500")
