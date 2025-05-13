# syntax=docker/dockerfile:1

FROM python:3.11

WORKDIR /code

COPY . .

ENV ENABLE_AZURE_MONITOR_TRACING=false

ENV AZURE_TRACING_GEN_AI_CONTENT_RECORDING_ENABLED=false

#ENV APP_LOG_FILE=app.log

RUN pip install --no-cache-dir --upgrade -r requirements.txt

EXPOSE 50505

CMD ["gunicorn", "api.main:create_app"]