FROM python:3.9-alpine3.16 

# Installs go here
RUN apk add py3-pip curl bash unzip
RUN pip install --upgrade pip


# Filesystem/folder stuff goes here
RUN mkdir -p /app/code
COPY . /app/code
WORKDIR /app/code


# RUN CHROMEDRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE` && \
#     mkdir -p /opt/chromedriver-$CHROMEDRIVER_VERSION && \
#     curl -sS -o /tmp/chromedriver_linux64.zip http://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip && \
#     unzip -qq /tmp/chromedriver_linux64.zip -d /opt/chromedriver-$CHROMEDRIVER_VERSION && \
#     rm /tmp/chromedriver_linux64.zip && \
#     chmod +x /opt/chromedriver-$CHROMEDRIVER_VERSION/chromedriver && \
#     ln -fs /opt/chromedriver-$CHROMEDRIVER_VERSION/chromedriver /app/code/data_collection


#RUN curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
#    echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list && \
#    apt-get -yqq update && \
#    apt-get -yqq install google-chrome-stable && \
#    rm -rf /var/lib/apt/lists/*


# Install latest version of ChromeDriver for Linux64 architecture
#RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
# unzip location is referenced in __main__.py and must match aht is here
#RUN unzip /tmp/chromedriver.zip chromedriver -d /app/code
# Add chromedriver to path 
#ENV PATH "$PATH:/app/code/data_collection"


# Pythone requirements
RUN python3 -m pip install -U pip
RUN python3 -m pip install -r requirements.txt --no-cache-dir

# Exit to test if everything till now compiles

CMD python3 __main__.py

# Actual execution
#CMD ["python3", "__main__.py"]