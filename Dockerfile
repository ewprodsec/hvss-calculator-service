# FROM python:3-alpine
# Use an official Python runtime as a parent image
FROM python:3.11-slim-buster

WORKDIR /app

COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
# CMD ["uvicorn", "app.main:app"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# Build the Docker Image
# IMAGE_NAME='hvss-calculator-service'
# IMAGE_REPO='ivanenko'
# TAG='latest'
# TAG='alpine'
# TAG='3-alpine'
# IMAGE_TAG="$IMAGE_REPO/$IMAGE_NAME:$TAG"
# echo $IMAGE_TAG

# sudo docker build -t $IMAGE_TAG .
# docker build -t ivanenko/hvss-calculator-service .

# docker run -it --rm -p 8088:8000 $IMAGE_TAG
# docker run -it --rm -p 8088:8000 ivanenko/hvss-calculator-service
