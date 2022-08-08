# Setting of Monitoring for JASECI #


## Prerequisite ##

### Install Helm  ###

We will use Helm Chart for installing our monitoring tools. Helm is widely known as "the package manager for Kubernetes".

https://helm.sh/docs/intro/install/


The Promethues and Grafana Stacks will be used as monitoring tools. We will start first by installing the Promethues pods in our cluster.

You can install pods in the same namespaces as your workload namespaces or you can also create a separate namespace for the monitoring pods.


## Promethues ##

#### Step 1 ####

##### add prometheus Helm repo  ####

First we will add chart repository reference in our local

```console
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
```

#### Step 2 ####

Then we will install the promethues service using below command.

If you are installing in your local kubernetes , run below command :

```console
 helm install prometheus prometheus-community/prometheus
```

If you are using Cloud , For example here we use AWS :

```console
 helm install prometheus prometheus-community/prometheus \
    --set alertmanager.persistentVolume.storageClass="gp2" \
    --set server.persistentVolume.storageClass="gp2"
```

After this run the Prometheus server can be accessed via port 80 on the following DNS name from within your cluster:
prometheus-server.\<namespace\>.svc.cluster.local

Here, in place of \<namespace\> put the name of namespace where your service lies. Note this URL for reference to put in Grafana setup later.

#### Step 3 ####

Run below command to check all the pods has been successfully created. This will create 5 pods

```console
kubectl get all
```


The 5 pods have different roles , as below :

Promethues-alert-manager - The Alertmanager handles alerts sent by client applications such as the Prometheus server. It takes care of deduplicating, grouping, and routing them to the correct receiver integration such as email, PagerDuty, or OpsGenie. It also takes care of silencing and inhibition of alerts.

promethueus-kube-state-metrics - kube-state-metrics (KSM) is a simple service that listens to the Kubernetes API server and generates metrics about the state of the objects. (See examples in the Metrics section below.) It is not focused on the health of the individual Kubernetes components, but rather on the health of the various objects inside, such as deployments, nodes and pods.

promethues-node-exporter - The Prometheus Node Exporter exposes a wide variety of hardware- and kernel-related metrics.

promethues-pushgateway - The Pushgateway is an intermediary service which allows you to push metrics from jobs which cannot be scraped. For details, see Pushing metrics.

promethues-server - It is the main promethues server pod which is responsible for all queries.


#### Step 4 ####

Use Port-forward to test if promethues is running in your local browser to check if all setup works and you are able to get the promethues running.

```console
kubectl port-forward deploy/prometheus-server 8080:9090
```




## Grafana ##


##### Go to grafana.yaml under grafana  Directory in the code and update the values of promethues URL as required #####

In the cloned repository folder , go to grafana/grafana.yaml file and update the URL to the promethues service URL as we noted doen in step 2 above, i.e prometheus-server.\<namespace\>.svc.cluster.local

Please note that in the previous example, we did not create any specific namespace for prometheus so the \<namespace\> here (and later) should be replaced with **default** if you follow the tutorial completely.

This is required to connect Grafana to collect data from promethues .

Now from the monitoring folder of the repo, run below command:


#### Step 1 ####

First we will add chart repository reference in our local

```console
helm repo add grafana https://grafana.github.io/helm-charts
```


#### Step 2 ####

If your running in your local kubernetes , run below :

Please Note to replace <YOUR PASSWORD> with the password you want to add for your grafana portal.

```console
helm install grafana grafana/grafana \
    --set adminPassword='<YOUR PASSWORD>' \
    --values grafana/grafana.yaml \
```
If you are using Cloud here, AWS :

```console
helm install grafana grafana/grafana \
    --set persistence.storageClassName="gp2" \
    --set persistence.enabled=true \
    --set adminPassword='<YOUR PASSWORD>' \
    --values helmcharts/grafana/grafana/grafana.yaml \
    --set service.type=LoadBalancer
```




#### Step 3 ####

Run the following command to check if Grafana is deployed properly and you can able to see running grafana pods:

```console
kubectl get all
```

#### Step 4 ####

Now, try to run grafana in your browser:

If you running in your local kubernetes, run below :

```console
kubectl port-forward deploy/grafana 80:3000
```


if you have used AWS Cloud, and with Load Balancer as in step 2 , you will get a Public External URL/OP


Run below code to get the External-IP for Grafana

```console
kubectl get svc grafana
```

#### Step 5 ####

Visit the URL from your Browser and login with credentials

Username : admin
password- "As given while applying grafana Helm"

#### Step 6 ####

For creating a dashboard to monitor the cluster:

## Cluster Monitoring Dashboard ##

Click '+' button on left panel and select ‘Import’.

Copy paste the json file in grafana-dashboards folder. 

Click ‘Load’.

Select ‘Prometheus’ as the endpoint under prometheus data sources drop down.

Click ‘Import’.

This will show monitoring dashboard for all cluster nodes

Generally, this dashboard contains a set of necessary panels. It monitors CPU and memory utilization for the nodes and for each pod. 

##### Credits https://www.eksworkshop.com/
