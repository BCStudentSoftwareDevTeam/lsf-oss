# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3

MAINTAINER Scott Heggen "heggens@berea.edu"

EXPOSE 8080

COPY ./requirements.txt /requirements.txt

WORKDIR /

RUN pip install -r requirements.txt

COPY . /
ENTRYPOINT [ "python" ]

CMD ["add_dummy_data.py"]

CMD [ "app.py" ]
