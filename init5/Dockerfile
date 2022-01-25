FROM python:3.10-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt update && apt -y dist-upgrade
RUN apt install -y netcat

RUN pip install --upgrade pip

COPY ./requirements.txt .
RUN pip install -r requirements.txt

RUN groupadd some_group && useradd -g some_group --shell /bin/bash --create-home app

ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

COPY . $APP_HOME

RUN chown -R app:some_group $APP_HOME

USER app

RUN chmod +x $APP_HOME/entrypoint.sh
ENTRYPOINT ["/home/app/web/entrypoint.sh"]