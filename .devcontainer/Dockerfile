FROM mcr.microsoft.com/vscode/devcontainers/base:ubuntu-22.04
USER root

# switch to https repo on firewall problem
RUN sed -i 's/http:/https:/g' /etc/apt/sources.list
RUN apt-get update

RUN apt update
RUN apt upgrade -y
RUN apt install -y python3-pip
