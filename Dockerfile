FROM centos:8

RUN dnf update -y && dnf install -y \
    epel-release \ 
    python3 \
    bind-utils \
    openssh-clients \
    python3-pip && dnf clean all -y

RUN pip3 install boto3 ansible

WORKDIR /gateway
COPY . /gateway

ENTRYPOINT ["/gateway/scripts/deploy.sh"]