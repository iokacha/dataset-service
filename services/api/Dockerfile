FROM python:3
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . /code
WORKDIR /code
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:8000"]