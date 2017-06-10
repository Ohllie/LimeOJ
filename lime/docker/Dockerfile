FROM ubuntu:16.04

RUN apt-get update
RUN apt-get install -y g++ python3 python3-pip curl

RUN pip3 install psutil

WORKDIR /sub
ADD docker_grader.py .

CMD ["python3", "docker_grader.py"]