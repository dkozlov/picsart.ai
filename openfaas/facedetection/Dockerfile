FROM ubuntu:18.10

ENV DEBIAN_FRONTEND noninteractive
ENV DEBCONF_NONINTERACTIVE_SEEN true

MAINTAINER Dmitry Kozlov <dmitry.kozlov@gigsternetwork.com>

# Install ubuntu base packages
RUN apt-get update
RUN apt-get install -y \
    python3-dev \
    python3-pip

#RUN pip3 install --upgrade pip \
#    && pip3 install flask \
#    && pip3 install pyyaml

RUN pip3 install flask \
    gevent \
    pyyaml

RUN apt update && apt install -y curl \
    && echo "Pulling watchdog binary from Github." \
    && curl -sSLf https://github.com/openfaas-incubator/of-watchdog/releases/download/0.4.5/of-watchdog > /usr/bin/fwatchdog \
    && chmod +x /usr/bin/fwatchdog

# Copy project files
WORKDIR /root
COPY . .

# Install requirements
WORKDIR mtcnn
RUN pip3 install -r requirements.txt \
    Pillow==5.3.0 \
    numpy \
    nose2 \
    coverage

# Install MTCNN 
RUN python3 setup.py install


WORKDIR /root

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

ENV write_debug="true"
ENV fprocess="python3 run_server.py"
ENV cgi_headers="true"
ENV mode="http"
ENV upstream_url="http://127.0.0.1:5000"
ENV exec_timeout=600s

HEALTHCHECK --interval=5s CMD [ -e /tmp/.lock ] || exit 1
CMD [ "fwatchdog" ]
