FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    git

RUN mkdir /webapp

WORKDIR /webapp

RUN git clone https://gitlab.com/lezz-git-it/webapp.git .

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

ENV DJANGO_DEBUG=False DJANGO_SECRET_KEY="52ipx7n#(65!mxn@d+_q0*n(^mxb8(c+-iqi36tu5%vgay-0n1"

EXPOSE 8000

RUN python manage.py collectstatic --no-input

CMD [ "gunicorn", "webapp.wsgi", "--bind=0.0.0.0" ]
