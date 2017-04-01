# This builds the happening-celery image. For consistency, environment variables
# and filesystem bindings should match those provided to the happening-web image
FROM python:3.4
MAINTAINER "jonathan@jscott.me"

RUN curl -sL https://deb.nodesource.com/setup_6.x | bash
RUN apt-get install -y git-all nodejs

# TODO: Restore this once we have stable tagging --branch latest

# This ensures that the latest version of the git code will be pulled - avoiding cache
ADD https://api.github.com/repos/happeninghq/happening/git/refs/heads/master version.json
RUN git clone https://github.com/happeninghq/happening.git happening

RUN pip3 install --upgrade pip
RUN pip3 install -r happening/src/requirements.txt
RUN cd happening/src && npm install && npm install -g webpack && webpack
RUN cd happening/src && python manage.py collectstatic --noinput

WORKDIR /happening/src
ENTRYPOINT ["python", "docker_celery_entry.py"]

EXPOSE 8000
