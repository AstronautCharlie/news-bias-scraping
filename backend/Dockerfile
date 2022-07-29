FROM python:3.9-alpine3.16 
RUN apk add py3-pip curl
RUN pip install --upgrade pip 
RUN mkdir -p /app/code 
COPY . /app/code 
WORKDIR /app/code 
RUN python3 -m pip install -U pip
RUN python3 -m pip install -r requirements.txt --no-cache-dir
CMD ["python3", "__main__.py"]