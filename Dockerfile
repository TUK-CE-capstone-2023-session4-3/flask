FROM python:3.8-slim


WORKDIR /Flask

RUN pip3 install flask 
RUN pip3 install opencv-python
RUN apt-get update
RUN apt-get -y install libgl1-mesa-glx
RUN apt-get -y  install libglib2.0-0


COPY . .


# RUN pip install --no-cache-dir -r requirement.txt

EXPOSE 8000

CMD ["python", "./main.py" ]