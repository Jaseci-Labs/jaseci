# Install Jaseci using Helm

### Prerequisite:

Install Helm in your Computer device



### Installing Jaseci

Update the Values.yaml files according to the requirement and then run below command

```bash

helm install jaseci .

```

### Installing Jaseci Ai Models

Its very easy to add any ai model you wish to add that uses Jaseci KIT docker image.

In values.yaml file, aimodels acts as a list of ai model you want to install with jaseci. Each model needs to be added below as a new object below aimodels like :

```bash

aimodels:

  - name: aimodel1
    ..........
    ..........
  - name: aimodel2
    ..........
    ..........

```

the variables of object need to be defined, an example below, you can copy it and change the values as needed

```bash

- name: js-use-qa
    script:
      - pip install jaseci-kit==1.3.3.19
      - uvicorn jaseci_kit.use_qa:serv_actions --host 0.0.0.0 --port 80    
    resources: 
      requests:
          memory: 2Gi
      limits:
          memory: 2Gi

```



###  Adding Ingress for Production workload.

For Production use case its better to activate Ingress for more secured and optimal usage.

To Activate, In values.yaml, Please update Ingress values as below

```bash

ingress:
  enabled: true   # to enabled ingress
  className: nginx-ingress   # Type of ingress controller, example nginx-ingress
  # annotations: add annotation for SSL , Add Cloud Specific annotions for SSL
  hosts:
    - host: test.xyz.com   # host URL for your jaseci services
      paths:
        - path: /
          pathType: Prefix


```

To Install Nginx-Controller, you can install it from below helm command

```bash
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update
helm install nginx-ingress ingress-nginx/ingress-nginx

```
