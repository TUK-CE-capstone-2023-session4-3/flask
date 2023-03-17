FROM python:3.8-slim


WORKDIR /Flask

RUN pip3 install flask 
RUN pip3 opencv-python

COPY . .


# RUN pip install --no-cache-dir -r requirement.txt

EXPOSE 8000

CMD ["python", "./main.py" ]