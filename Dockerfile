FROM nginx/unit:1.28.0-python3.10

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt .
RUN pip install gunicorn
RUN python -m pip install -r requirements.txt

WORKDIR /code
COPY . /code
RUN mkdir /srv/bitmorpher
COPY static /srv/bitmorpher/
COPY unit.json /var/lib/unit/conf.json

RUN mkdir logs
RUN python manage.py makemigrations
RUN python manage.py migrate

RUN python manage.py collectstatic --no-input

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi:application"]
