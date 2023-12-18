FROM jenkins/jenkins:lts

USER root

RUN apt-get update

RUN apt install -y python3

RUN apt-get update && \
    apt-get install -y docker.io && \
    rm -rf /var/lib/apt/lists/*