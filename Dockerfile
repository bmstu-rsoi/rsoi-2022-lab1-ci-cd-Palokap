FROM python:3.9
COPY lab/ /lab
COPY requirements.txt /lab
WORKDIR /lab
RUN pip install -r requirements.txt
CMD ["python3", "app.py"]