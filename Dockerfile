FROM python:3.10.8-slim
LABEL mainteiner="hapyto371@gmail.com"

ENV PYTHONBUFFERED 1

WORKDIR app/

COPY requirements.txt requirements.txt

RUN apt-get update \
    && apt-get -y install  \
    libpq-dev  \
    gcc  \
    binutils  \
    libproj-dev  \
    gdal-bin \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt

COPY . .

RUN adduser --disabled-password --no-create-home django-user
RUN mkdir -p /vol/web/media
RUN chown -R django-user:django-user /vol/
RUN chmod -R 755 /vol/web/

USER django-user
