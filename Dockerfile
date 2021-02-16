FROM python:3.6-slim
RUN apt-get update && apt-get install git -y
RUN mkdir -p /usr/share/man/man1
RUN apt-get install -y --no-install-recommends openjdk-11-jre
RUN pip3 install --user --upgrade git+https://github.com/twintproject/twint.git@origin/master#egg=twint
RUN pip3 install --user pyspark
