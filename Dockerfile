FROM ubuntu:14.04.3
MAINTAINER jysong@soundlifetv.com
RUN locale-gen en_US.UTF-8
ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en

RUN rm -f /etc/apt/sources.list
ADD develop/trusty /etc/apt/sources.list.d

RUN apt-get update -y
RUN apt-get upgrade -y

RUN apt-get install -y \
      python-dev \
      python-pip \
      libxml2-dev \
      libxslt1-dev \
      zlib1g-dev \
      libffi-dev \
      libssl-dev \
      polipo \
      supervisor \
      python-pip \
      git

ADD develop/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
ADD . /srv/spiderserver/
RUN mkdir -p /srv/spiderserver/logs
WORKDIR /srv/spiderserver

RUN pip install -i 'http://mirrors.aliyun.com/pypi/simple' -r requirements.txt

EXPOSE 8600

ENTRYPOINT ["/usr/bin/supervisord"]
CMD ["-c", "/etc/supervisor/conf.d/supervisord.conf"]
