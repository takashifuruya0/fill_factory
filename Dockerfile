FROM python:3.9
ENV PYTHONUNBUFFERED 1
RUN apt update && apt dist-upgrade -y && apt clean
ADD requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY ./ /home/fill_factory
WORKDIR /home/fill_factory