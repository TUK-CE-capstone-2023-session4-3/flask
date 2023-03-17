FROM python:3.8-slim


WORKDIR /Flask

RUN pip3 install flask 

COPY . .


# RUN pip install --no-cache-dir -r requirement.txt
RUN pip3 install cv2

EXPOSE 8000

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]