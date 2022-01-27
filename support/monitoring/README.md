# Setting of Monitoring for JASECI #


## Prerequisite ##

### Install Helm  ###

https://helm.sh/docs/intro/install/



## Promethues ##

#### Step 1 ####

##### add prometheus Helm repo  #####
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts

#### Step 2 ####

helm install prometheus prometheus-community/prometheus \
    --set alertmanager.persistentVolume.storageClass="gp2" \
    --set server.persistentVolume.storageClass="gp2"

The Prometheus server can be accessed via port 80 on the following DNS name from within your cluster:
prometheus-server.prometheus.svc.cluster.local

#### Step 3 ####

kubectl get all

#### Step 4 ####

Use Port-forward to test if promethues is running in your local browser

kubectl port-forward -n prometheus deploy/prometheus-server 8080:9090




## Grafana ##


##### Go to grafana.yaml under grafana  Directory in the code and update the values of promethues URL as required #####


#### Step 1 ####

helm install grafana helmcharts/grafana \
    --set persistence.storageClassName="gp2" \
    --set persistence.enabled=true \
    --set adminPassword='<YOUR PASSWORD>' \
    --values helmcharts/grafana/grafana/grafana.yaml \
    --set service.type=LoadBalancer


    Please Note to give your password while applying the same

#### Step 3 ####

Run the following command to check if Grafana is deployed properly:

kubectl get all -n grafana

#### Step 4 ####

Run below code to get the External-IP for Grafana

kubectl get svc grafana

#### Step 5 ####

Visit the URL from your Browser and login with credentials

Username : admin
password- "As given while applying grafana Helm"

#### Step 6 ####

For creating a dashboard to monitor the cluster:

## Cluster Monitoring Dashboard ##

Click '+' button on left panel and select ‘Import’.

Enter 3119 dashboard id under Grafana.com Dashboard.

Click ‘Load’.

Select ‘Prometheus’ as the endpoint under prometheus data sources drop down.

Click ‘Import’.

This will show monitoring dashboard for all cluster nodes

## Pods Monitoring Dashboard ##

Click '+' button on left panel and select ‘Import’.

Enter 6417 dashboard id under Grafana.com Dashboard.

Click ‘Load’.

Enter Kubernetes Pods Monitoring as the Dashboard name.

Click change to set the Unique identifier (uid).

Select ‘Prometheus’ as the endpoint under prometheus data sources drop down.s

Click ‘Import’.






##### Credits https://www.eksworkshop.com/