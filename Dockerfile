FROM python:3.9-buster

WORKDIR /app

USER maid

COPY requirements.txt .
RUN pip install -r /app/requirements.txt

COPY . .
CMD ["python", "maid_ritsu"]