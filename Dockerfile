FROM python:3.11

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential default-libmysqlclient-dev

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

# Collect static files for production use
RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi:application"]
