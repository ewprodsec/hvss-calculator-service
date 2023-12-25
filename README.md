# HVSS&copy; Calculator Web Service

This open source project aims to promote adoption of the Healthcare Vulnerability Scoring System (HVSS) &copy; through an easy to use and integrate reference implementation.

The HVSS&copy; Calculator Web Service provides a simple web application to interact with the [HVSS&copy; Calculator Machine Learning (ML) Models](https://github.com/ewprodsec/hvss-calculator-lab).

The project includes both frontend and backend components:
- The frontend is a vanilla HTML, JavaScript, and CSS application for simplicity.
- The backend uses Python (FastAPI) to implement a REST API. This allows the frontend to be replaced or for the API to be leveraged by other workflows.
- The interactive API documentation using OpenAPI and ReDoc for discoverability.
- The Dockerfile and [public container image](https://hub.docker.com/r/ewproductsecurity/hvss-calculator-service) available on Docker Hub to facilitate containerized deployment.
- The container image is self-contained and dependency-free, allowing for easy local runtime execution.

## HVSS&copy; Calculator Machine Learning (ML) Models

The HVSS&copy; Calculator ML models are a core component of the current HVSS calculator implementation.

This project utilizes pre-built and ready-to-use models located in the `./hvss_calc/Models` directory. These models will be upgraded as new versions become available at the original [HVSS Machine Learning Training Lab](https://github.com/ewprodsec/hvss-calculator-lab) project.


## How to Build, Publish and Run the Docker Image

### Build

~~~~sh
# Build the Docker Image
IMAGE_NAME='hvss-calculator-service'
IMAGE_REPO='ewproductsecurity'
IMAGE_TAG="$IMAGE_REPO/$IMAGE_NAME:latest"
echo $IMAGE_TAG

docker build -t $IMAGE_TAG .
# or just
docker build -t ewproductsecurity/hvss-calculator-service:latest
~~~~

### Publish

~~~~sh
# Push a new tag/image to the repository
echo $IMAGE_TAG

# docker login [OPTIONS] [SERVER]
docker login -u <your-docker-login>

docker push $IMAGE_TAG
# or just
docker push ewproductsecurity/hvss-calculator-service:latest
~~~~

### Pull

~~~~sh
# Pull the image from the repository
echo $IMAGE_TAG
docker pull $IMAGE_TAG
# or just
docker pull ewproductsecurity/hvss-calculator-service:latest
~~~~

### Run the Docker Container

~~~~sh
# Run the Docker Container
PORT='8088'

docker run -it --rm -p $PORT:8000 $IMAGE_TAG
# or just
docker run -it --rm -p 8088:8000 ewproductsecurity/hvss-calculator-service:latest

# -d - run as a daemon
docker run -it -d --rm -p $PORT:8000 $IMAGE_TAG
# or just
docker run -it -d --rm -p 8088:8000 ewproductsecurity/hvss-calculator-service:latest
~~~~

- Open the Calculator web app: <http://localhost:8088/>
- Interactive API Documentation ([Swagger UI](https://github.com/swagger-api/swagger-ui)): <http://localhost:8088/docs>
- Alternative Interactive API Documentation ([ReDoc](https://github.com/Redocly/redoc)): <http://localhost:8088/redoc>


## Development Time Notes

### Environment

````sh
python -V
# Python 3.11.3
pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt
````

### Unit Tests and Test Reports

To avoid pytest `Module not found` error even if module exists, call `python -m pytest` instead of just `pytest`:

````sh
python -m pytest -v

pip install pytest-html
python -m pytest -v --html=report.html
````

### Run Dev Server

````sh
# start Uvicorn (a simple ASGI web server for Python)
uvicorn main:app --reload
````

- Open web UI <http://127.0.0.1:8000/>
- Simplified UI is available at: <http://127.0.0.1:8088/simple>
- Interactive API Documentation ([Swagger UI](https://github.com/swagger-api/swagger-ui)): <http://127.0.0.1:8000/docs>
- Alternative Interactive API Documentation ([ReDoc](https://github.com/Redocly/redoc)): <http://127.0.0.1:8000/redoc>


## Known Bugs and TODO

- Disable sending S:U to the backend


## Support

The source code of the project is provided on "as is" terms with no warranty (see license for more information). Do not file Github issues with generic support requests.


## License

This project is released under the terms of the GNU Lesser General Public License (LGPL). See LICENSE file for details.


## Acknowledgments
This project was originally created by the HVSS Working Group, founded by the Product Security Team of [Edwards Lifesciences](https://www.edwards.com):
- Oleg Yusim
- Jacob Barkai
- Roman Ivanenko
- Samuel Takachicha
- Tejas Bharambe
- Vinitha Mathiyazhagan
- Maddy Tamilthurai
- Aleksey Haytman
- Isaias Rivera
