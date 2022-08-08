# INSTALLING ELK STACK ON JASECI 


## Installing Elastci Search

Use the Elastic helm Chart in this Repository to install ElasticSearch as it has been modified for single node Setup.

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