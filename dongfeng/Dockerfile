FROM debian:jessie
MAINTAINER Seah Ying Cong <yingcong@glints.com>

ENV DEBIAN_FRONTEND noninteractive

# Update repositories
RUN apt-get update && apt-get install -y netcat curl bzip2 gcc libblas-dev liblapack-dev libatlas-base-dev build-essential gfortran libfreetype6 libfontconfig&& \
    apt-get install --no-install-recommends -y git && \
    apt-get clean

# Install python and pip
RUN apt-get install --no-install-recommends -y git python2.7-dev python-pip

# Install Node.js & npm
RUN curl -sL https://deb.nodesource.com/setup_5.x | bash -
RUN apt-get --no-install-recommends -y install nodejs

# Install CasperJS
RUN npm install -g casperjs && \
    npm cache clean

ENV PATH $PATH:/usr/lib/node_modules/casperjs/node_modules/phantomjs/lib/phantom/bin

# Load our code in
RUN mkdir -p /app
WORKDIR /app
ADD . /app

# Install python dependencies
RUN pip install -r requirements.txt
RUN python -m nltk.downloader wordnet

CMD ["python", "app.py"]
