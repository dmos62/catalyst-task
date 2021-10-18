FROM python:3.9.1
ADD . /python-flask
WORKDIR /python-flask
RUN pip3 install -r requirements.txt

ENTRYPOINT [ "python3" ]

CMD [ "main.py" ]
