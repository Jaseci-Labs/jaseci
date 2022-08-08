# INSTALLING ELK STACK ON JASECI 

For installing ELK, we need to first add the reference for the helm repository in our local

```bash
helm repo add elastic https://helm.elastic.co
```


## Installing Elastci Search

Use the Elastic helm Chart in this Repository to install ElasticSearch as it has been modified for single node Setup unlike available in elastic helm chart repo.

```bash

helm install elasticsearch elastic/elasticsearch

```

Please wait for ElasticSearch pods to get started and Running


## Installing Kibana

To install Kibana on top of Elasticsearch, type the following command:

```bash
helm install kibana elastic/kibana
```

For accessing Kibana , Port forward it to port you want to access

```bash

kubectl port-forward deployment/kibana-kibana 5601

```

## Installing Filebeat

```bash
helm install kibana elastic/filebeat
```

## Installing Logstash

```bash
helm install logstash elastic/logstash
```