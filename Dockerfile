FROM python:3.8.5

WORKDIR /code
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
CMD python /code/manage.py runserver 0:8000
