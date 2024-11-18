FROM ubuntu:18.04

RUN apt-get update && apt-get install -y curl apt-transport-https lsb-release gnupg2
RUN curl -s https://packages.xcyber360.com/key/GPG-KEY-XCYBER360 | apt-key add - && \
    echo "deb https://packages.xcyber360.com/3.x/apt/ stable main" | tee /etc/apt/sources.list.d/xcyber360.list && \
    apt-get update && apt-get install xcyber360-agent=3.13.2-1 -y
