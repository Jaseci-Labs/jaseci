# lifelogify

[Please visit LifeLogify wiki for guidelines on coding](https://wiki.lifelogify.com/)

## Getting Started

Let's get everything up and running!

### Assumptions

- You have a kubernetes environment linked to `kubectl` command.
  - Docker Desktop is recommeneded and tested although minikube and microk8s should be fine
- You have npm and Node js installed in the environment you will be working with the web client
- Assuming you're running commands from the base directory of lifelogify codebase.

### High Level Process for Bringing up Dev Instance

1. First the backend must be deployed in your k8 environment.

   `kubectl apply -f scripts/kube_manifests/jaseci.yaml`

2. Then forward to localhost port 8000

   `kubectl port-forward service/jaseci 8000:80 &`

3. Then change to web client director and run npm i to install all npm packages required by client

   `cd frontend/web; npm i`

4. Then run npm start!

   `npm start`

5. Done!
