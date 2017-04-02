Happening
=========

[![Build Status](https://travis-ci.org/happeninghq/happening.svg?branch=master)](https://travis-ci.org/happeninghq/happening)
[![Requirements Status](https://requires.io/github/happeninghq/happening/requirements.svg?branch=master)](https://requires.io/github/happeninghq/happening/requirements/?branch=master)
[![Coverage Status](https://coveralls.io/repos/github/happeninghq/happening/badge.svg?branch=master)](https://coveralls.io/github/happeninghq/happening?branch=master)
[![Documentation Status](https://readthedocs.org/projects/happening/badge/?version=latest)](https://readthedocs.org/projects/happening/?badge=latest)


Happening is an open source event/community management tool.

Think Eventbrite meets Meetup, running on your own domain with your own branding.

We're in active development and Happening is not recommended for production use. Pull requests are welcomed.

Documentation is available on [ReadTheDocs](https://happening.readthedocs.org).

We use docker for development and distribution.

To launch a fully configured Happening instance use ``docker-compose up`` from within the src directory. Media will be stored in the media directory, plugins can be placed in the plugins directory, and database data is stored in a docker volume (see the docker-compose file). Once this is running, visit http://localhost:8000 and use the username ``admin`` and password ``password``. For production it is recommended that you run nginx in front of the happening web server.