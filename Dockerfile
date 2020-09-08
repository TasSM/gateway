FROM centos:8

RUN dnf update -y && dnf install -y \
    epel-release \ 
    python3 \
    python3-pip \
    ansible && dnf clean all -y

RUN pip3 install boto3



