# Production Mode YAML

## Install Specific version of jaseci KIT model in the POD

To install Specific version of jaseci KIT, Follow below process.
The use_qa.yaml ConfigMAP has environmnet variable declared as $version , which we will substitute while applying the Yaml 


### Export environment variable 

```bash
export version= {version no}  i.e 1.3.3.16

```

### Install docker

Run below command to apply the use_enc.yaml/use_qa.yaml to substitute the value of version in Config Map
```bash
envsubst < use_qa.yaml | kubectl apply -f -
```
