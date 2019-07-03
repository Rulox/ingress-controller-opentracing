FROM ubuntu:latest

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "app.py"]
