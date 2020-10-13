FROM python:3.6

# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# install chromedriver
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# install xvfb
RUN apt-get install -yqq xvfb

# set display port and dbus env to avoid hanging
ENV DISPLAY=:99
ENV DBUS_SESSION_BUS_ADDRESS=/dev/null

# install selenium
RUN pip install selenium==3.8.0
RUN pip install flask
RUN pip install flask_cors
RUN pip install beautifulsoup4
RUN pip install moment
RUN pip install requests
RUN pip install pymongo==3.5.1
RUN pip install pika
RUN pip install mysql-connector-python

COPY run.sh /
COPY setting.py /
COPY multiprocess.py /
COPY api.py /

RUN chmod a+x /run.sh

CMD "/run.sh"