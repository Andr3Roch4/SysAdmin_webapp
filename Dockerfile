FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    git

RUN mkdir /webapp

WORKDIR /webapp

COPY . /webapp

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

RUN python manage.py collectstatic --no-input

CMD [ "gunicorn", "webapp.wsgi", "--bind=0.0.0.0" ]
