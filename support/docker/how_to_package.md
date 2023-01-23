# How-to create a release/deployment package for your jac program

In this guide, we will walk through our recommended way of packaging up everything required to deploy your jac program in one package.
The package should include:
* a docker image for the jaseci server (w/ pre-trained AI models built-in if applicable)
* a jsctl script to intialize your server
* a README with instructions on how to use the docker image and jsctl script

## Docker image
### Select the right base image
Before building our custom docker image, we first need to select a base docker image.
We provide a set of base docker images, hosted on [docker hub](https://hub.docker.com/u/jaseci).
* `jaseci/jaseci` conatins only `jaseci_core` and `jaseci_serv`. It does not contain any modules from `jaseci_ai_kit`. So if your jac program does not require any modules from AI kit, you can use this base image.
* `jaseci/jac-*` are the base images with the corresponding AI kit package built-in. For example, `jaseci/jac-nlp` contains the modules in the `jac-nlp` package. Select according to what your jac program needs.

### Create dockerfile for our custom image
Now that we have selected the right base image (we will use `jaseci/jac-nlp` for this guide), we will now create a custom dockerfile for our custom image.

Here is a template dockerfile to start with:

```dockerfile
# Specify your base image
FROM jac-nlp:1.4.0.6

# Set working directory. / is fine for most scenarios.
WORKDIR /

# Install any linux dependencies
ENV DEBIAN_FRONTEND=nointeractive
RUN apt -y update; apt -y install --no-install-recommends CUSTOM_APT_PACKAGES_GO_HERE

# Copy any pre-trained models required for the jac program.
COPY ./pretrained_bi_enc /pretrained_bi_enc
```
Save the docker file to a file and let's call it `my_jac.Dockerfile`.

For additional questions on the syntax in this dockerfile, refer to the [Docker documentation](https://docs.docker.com/engine/reference/builder/).

### Build the image
To build the image, run
```bash
docker build -t {IMAGE_NAME} -f my_jac.Dockerfile .
```
Note that there is a period `.` at the end of this command.

Also, replace `{IMAGE_NAME}` with what you want to name your docker image.


### Share the image
After the build finishes, you can check the size of your docker image with
```bash
docker image ls
```

There are multiple ways to share a docker image.
The most common and recommended way is through a docker image registry (e.g., dockerhub).
You can also share the image directly as a file.
[Here](https://medium.com/@sanketmeghani/docker-transferring-docker-images-without-registry-2ed50726495f) is a short tutorial on how that.

## JSCTL script
Deploying a jac program on a fresh Jaseci server requires a few setup steps.
To faciliate this, we recommend setting up a JSCTL script as a companion to the docker image.

A JSCTL script is simply a plain text file with a list of jsctl commands.

For example, the follow series of commands (or similiar) are commonly needed to initialize a jac program.

```bash
jac build main.jac
login JASECI_URL ---username UERNAME --password PW
sentinel register -mode jir main.jir
actions load module jac_nlp.use_enc
```

Save this in a file and name it `init_script`. To use this script, run
```bash
jsctl script init_script
```

## README
A README.md should be packaged together with the docker image and the jsctl script.

This README should contain, at minimum, the following:
* Manifest of the content of this package (the docker image, jsctl script, etc.)
* Description of the docker image. For example, what it contains.
* Instructions on using the docker image to deploy a jsserv server.
    * This part can vary depending on the desired deployment environment and approach (e.g. docker vs k8s vs cloud). What we should explain at the minimum, is that the docker image contains all the dependencies of Jaseci and AI models required for the application and the the following commands start a `jsserv` server
    ```bash
    jsserv makemigrations base
    jsserv makemigrations
    jsserv migrate
    jsserv runserver 0.0.0.0:80
    ```
    * [Here](https://github.com/Jaseci-Labs/jaseci/blob/main/scripts/jaseci.yaml) is an example kubernetes manifest yaml file that can be shared as a reference if kuberentes deployment is desired.
* Instructions on how to use the JSCTL script. The section above in this guide is sufficient in most cases.
* Expected behavior of the application. What should a new user try to test if their deployment is successful? Example walker runs and expected response should be included.
* Any additional information you would like to include about the application.
