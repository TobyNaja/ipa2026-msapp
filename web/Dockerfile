FROM python
WORKDIR /home/myapp

COPY ./templates/* /home/myapp/templates/
COPY ./static/* /home/myapp/static/
COPY ./app.py /home/myapp/
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install flask

CMD ["python", "/home/myapp/app.py"]
EXPOSE 8080