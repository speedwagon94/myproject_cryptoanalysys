FROM python:3.11

SHELL ["/bin/bash", "-c"]

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /app

RUN pip install --upgrade pip

WORKDIR /app

RUN mkdir -p /cryptoapp/static

RUN mkdir -p /cryptoapp/media

RUN pip install -r requirements.txt

RUN python manage.py migrate

RUN python manage.py collectstatic --noinput

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
