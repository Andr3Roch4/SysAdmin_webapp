FROM python:3.12-slim

RUN mkdir -p /webapp && \
    groupadd -r grupo3 && \
    useradd --no-log-init -r -g grupo3 -d /webapp grupo3 && \
    chown grupo3:grupo3 /webapp

WORKDIR /webapp

COPY --chown=grupo3:grupo3 . .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

RUN python manage.py collectstatic --no-input --no-post-process && \
    chown -R grupo3:grupo3 /webapp/staticfiles

USER grupo3

CMD [ "gunicorn", "webapp.wsgi", "--bind=0.0.0.0" ]
