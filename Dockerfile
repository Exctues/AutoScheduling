FROM python:3

ADD Backend/ /Backend/
ADD static/ /static/
ADD u_csv/ /u_csv/
ADD CATt/ /CATt/
ADD manage.py /
ADD ./requirements.txt /requirements.txt

RUN pip3 install -r requirements.txt
EXPOSE 8080

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8080"]
