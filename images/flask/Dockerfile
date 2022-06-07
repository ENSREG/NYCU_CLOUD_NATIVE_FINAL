FROM python:3.8-slim
COPY . /sample_crawler
WORKDIR /sample_crawler

ARG UID
ARG UserName

#RUN useradd -m ${UserName} -u ${UID} &&\
#    adduser ${UserName} sudo &&\
#    apt-get update &&\
#    apt-get -y upgrade &&\
#    apt-get install -y git net-tools vim sudo tcsh gcc g++ unzip&&\
#    apt-get clean

#USER ${UserName}

RUN  apt-get update \
  && apt-get install -y wget \
  && rm -rf /var/lib/apt/lists/*
RUN wget https://raw.githubusercontent.com/ianchen0119/NYCU_CLOUD_NATIVE_FINAL/master/images/crawler/data/Pred.csv
RUN wget https://raw.githubusercontent.com/ianchen0119/NYCU_CLOUD_NATIVE_FINAL/master/images/crawler/data/GroundTruth.csv
RUN pip install -r ./requirements.txt
CMD ["python","run.py"]

EXPOSE 8080