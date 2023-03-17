FROM python:3.8-slim

COPY . /flask

RUN pip3 install flask 

WORKDIR /Flask

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]