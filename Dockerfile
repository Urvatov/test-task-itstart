FROM python:3.9

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

#CMD ["python", "test.py"]

#127.0.0.1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]