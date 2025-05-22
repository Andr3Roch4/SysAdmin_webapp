FROM python:3.12-slim

RUN groupadd -r grupo3 && useradd --no-log-init -r -g grupo3 grupo3


RUN mkdir /webapp

WORKDIR /webapp

COPY . /webapp

USER grupo3

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

RUN python manage.py collectstatic --no-input

CMD [ "gunicorn", "webapp.wsgi", "--bind=0.0.0.0" ]
