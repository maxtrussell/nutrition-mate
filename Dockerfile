FROM python:3.7

EXPOSE 5000

ADD . /nutrition-mate
WORKDIR /nutrition-mate

RUN pip install -r requirements.txt
CMD ["python", "server.py"]
