To add a new AI service, follow the steps below:

1. Run `./create_ai_service.sh` with the AI service name in CamelCase. For example, `./create_ai_service.sh XLNet`.
    * This script will set up the scaffolding required for the new service.
2. Follow the output prompted by the previous step, including:
   1) Add steps in Dockerfile to download and prepare any pre-trained model files. Follow the TODOs.
   2) Update requirements.txt with python dependencies required for your model."
   3) Fill in the rest of the code in the service code in the flask python file. Follow the TODOs.
   4) Take a look at the k8s manifest yaml file. You might need to update the memory limit and/or port.
   5) Build the docker image with `docker build -t IMAGE-NAME -f Dockerfile`"
   6) Finally, test the service by applying the manifest `kubectl apply -f K8S-YAML`"
