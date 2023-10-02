# HVSS Calculator Backend Service

## Build, Publish and Run the Docker Image

### Build

~~~~sh
# Build the Docker Image
IMAGE_NAME='hvss-calculator-service'
IMAGE_REPO='ivanenko'
IMAGE_TAG="$IMAGE_REPO/$IMAGE_NAME:latest"
echo $IMAGE_TAG

docker build -t $IMAGE_TAG .
~~~~

### Publish

~~~~sh
# Push a new tag/image to the repository
echo $IMAGE_TAG

# docker login [OPTIONS] [SERVER]
docker login -u <your-docker-login>

docker push $IMAGE_TAG
~~~~

### Pull

~~~~sh
# Pull the image from the repository
echo $IMAGE_TAG
docker pull $IMAGE_TAG
# or
docker pull ivanenko/hvss-calculator-service
~~~~

### Run the Docker Container

~~~~sh
# Run the Docker Container
PORT='8088'

docker run -it --rm -p $PORT:8000 $IMAGE_TAG
docker run -it --rm -p 8088:8000 ivanenko/hvss-calculator-service

# -d - run as a daemon
docker run -it -d --rm -p $PORT:8000 $IMAGE_TAG
docker run -it -d --rm -p 8088:8000 ivanenko/hvss-calculator-service
~~~~

- Open the Calculator web app: <http://localhost:8088/>
- Interactive API Documentation ([Swagger UI](https://github.com/swagger-api/swagger-ui)): <http://localhost:8088/docs>
- Alternative Interactive API Documentation ([ReDoc](https://github.com/Redocly/redoc)): <http://localhost:8088/redoc>

---

## Development

### Environment

````sh
python -V
# Python 3.11.3
pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt
````

### Unit Tests and Test Reports

To avoid pytest 'Module not found' error even if module exists, call `python -m pytest` instead of just `pytest`:

````sh
python -m pytest -v

pip install pytest-html
python -m pytest -v --html=report.html
````

### Run

````sh
uvicorn main:app --reload

#http://127.0.0.1:8000/

#Check the Interactive API Documentation
#http://127.0.0.1:8000/docs

````

- Open web UI <http://127.0.0.1:8000/>
- Simplified UI is available at: <http://127.0.0.1:8088/simple>
- Interactive API Documentation ([Swagger UI](https://github.com/swagger-api/swagger-ui)): <http://127.0.0.1:8000/docs>
- Alternative Interactive API Documentation ([ReDoc](https://github.com/Redocly/redoc)): <http://127.0.0.1:8000/redoc>

## TODO

- Disable sending S:U to the backend
