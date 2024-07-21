FROM python:3.10

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
COPY ./app /app
COPY ./scripts /scripts

WORKDIR /app
EXPOSE 8000

RUN python -m venv /python && \
    /python/bin/pip install --upgrade pip && \
    apt-get update && \
    apt-get install -y postgresql-client && \
    /python/bin/pip install -r /requirements.txt && \
    apt-get clean && \
    adduser --disabled-password --no-create-home admin && \
    mkdir -p /vol/web/static && \
    mkdir -p /vol/web/media && \
    chown -R admin:admin /vol && \
    chmod -R 755 /vol && \
    chmod -R +x /scripts

ENV PATH="/scripts:/python/bin:$PATH"

USER admin

CMD ["run.sh"]