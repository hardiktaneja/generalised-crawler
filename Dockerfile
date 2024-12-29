FROM ubuntu:22.04

# Upgrade installed packages
RUN apt-get update && apt-get upgrade -y && apt-get clean

# (...)

# Python package management and basic dependencies
RUN apt-get install -y curl python3.11 python3.11-dev python3.11-distutils

# Register the version in alternatives
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1

# Set python 3 as the default python
RUN update-alternatives --set python /usr/bin/python3.11

# Install pip for Python3.7
RUN curl -s https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
    python3.11 get-pip.py --force-reinstall && \
    rm get-pip.py

RUN python --version
RUN pip3 --version
COPY requirements.txt /
RUN pip --version
RUN pip3 install --upgrade pip
RUN pip3 install -r /requirements.txt

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2


COPY . /home/ubuntu/
WORKDIR /home/ubuntu/


RUN chmod +x /home/ubuntu/gunicorn_starter.sh
RUN echo "$LS"
RUN pwd
RUN ls

EXPOSE 5000
ENTRYPOINT ["./gunicorn_starter.sh"]
