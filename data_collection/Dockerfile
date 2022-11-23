FROM python:3.9-alpine3.16 

# Installs go here
RUN apk add py3-pip curl bash unzip
RUN pip install --upgrade pip

# Filesystem/folder stuff goes here
RUN mkdir -p /app/code
COPY . /app/code
WORKDIR /app/code

# Pythone requirements
RUN python3 -m pip install -U pip
RUN python3 -m pip install -r requirements.txt --no-cache-dir 

CMD ["python3", "__main__.py"]