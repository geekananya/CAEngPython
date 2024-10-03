# base image on top of which application will be run
FROM python:3.12.6

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

ENV PYTHONUNBUFFERED=1

EXPOSE 8000

# CMD ["python3", "manage.py", "migrate",
#  &&
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
# CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]