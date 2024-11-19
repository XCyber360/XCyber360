# Xcyber360 Docker Copyright (C) 2017, Xcyber360 Inc. (License GPLv2)
FROM amazonlinux:2023

RUN yum install curl-minimal openssl -y &&\
yum clean all

WORKDIR /

COPY config/entrypoint.sh /

RUN chmod 700 /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]