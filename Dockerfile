FROM python:3

WORKDIR /usr/src/app

# install python dependencies
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt && pip install uWSGI==2.0.15

COPY archive_to_ia /usr/src/app/archive_to_ia
COPY uwsgi.ini /usr/src/app/

EXPOSE 8080
ENV PYTHONPATH /usr/src/app
ENV FLASK_APP archive_to_ia
ENV APP_CONFIG_PATH /data/config/config.json

CMD ["uwsgi", "--ini", "uwsgi.ini"]
