# Dockerfile
FROM ubuntu:22.04

RUN apt-get update && apt-get install -y python3
RUN apt-get update && apt-get install -y python3-pip

WORKDIR /app

COPY requirements.txt requirements.txt

RUN apt-get update && apt-get install -y uvicorn
                                                                                                                                                                          
RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]
