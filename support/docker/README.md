## Jaseci Docker Images

There are two version of the Jaseci docker image and they are both built using the `jaseci.Dockerfile` in this directory.

Note: docker images are automatically built and pushed to dockerhub on tagging by the github actions. 

### Full Jaseci image
To build the full jaseci docker image, which include the core Jaseci package (`jaseci`), the Jaseci server (`jaseci-serv` or `jsserv`) and the AI models in the Jaseci AI Kit (`jaseci-ai-kit`), run the following
```
docker build -t jaseci/jaseci-ai:1.3.5.22 \
    --build-arg JASECI_PYPI_VERSION=1.3.5.22 \
    --build-arg JASECI_SERV_PYPI_VERSION=1.3.5.22 \
    --build-arg JASECI_AI_KIT_PYPI_VERSION=1.3.5.22 \
    --build-arg BUILD_WITH_AI=1 \
    -f jaseci.Dockerfile .
```

### Core Jaseci image, sans Jaseci AI Kit packages
To build the core jaseci image that does not include the Jaseci AI Kit packages, build without the `BUILD_WITH_AI` argument.
```
docker build -t jaseci/jaseci-ai:1.3.5.22 \
    --build-arg JASECI_PYPI_VERSION=1.3.5.22 \
    --build-arg JASECI_SERV_PYPI_VERSION=1.3.5.22 \
    -f jaseci.Dockerfile .
```