This is a fork of this repo: https://github.com/vgeorgework/Flaskdemo - cleaned up, since it initially didn't run.

Flask, MySQL and kubernetes demo.

This is a template deployment repo which has a scraper pod which creates dummy values, puts them in a database (SQL). The database is available externally, including login template.

Local development can be tested with minikube, and it can be deployed using helm charts to the cloud (using google cloud for now).

## Pre-requisites

- [Minikube](https://minikube.sigs.k8s.io/docs/start/) installed and running.
- Virtualization enabled in the host.
- [Docker](https://docs.docker.com/engine/install/) installed.
- [Helm](https://helm.sh/docs/intro/install/) installed.
- [Kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/) CLI installed.

## Custer Architecture
![Cluster Architecture image](https://github.com/)

![Kubernetes pods image](https://github.com/)

##  Summary
The Flask app image, built using the Dockerfile, is pushed to a public Docker Hub repository (flaskapp). In the Kubernetes cluster, a Flask app service is created to route traffic to frontend pods, which are managed by a ReplicaSet. The MySQL service is deployed using a StatefulSet, with the MySQL pod utilizing a Persistent Volume Claim (PVC) to request storage from a Persistent Volume (PV). The cluster also sets up ConfigMaps and Secrets to manage environment variables securely. The entire deployment is orchestrated using a Helm chart.


## To run this project execute below commands using minikube.<br />

```
# Start minikube
minikube start

# Connect minikube to docker
eval $(minikube docker-env)

# Build the required docker images - flask app and scraper.
cd flaskapp
docker build . -t nhutton/flask_test_app:0.9 -f ./Dockerfile
cd ../scraper
docker build . -t nhutton/scraper_test_app:0.9 -f ./Dockerfile

# If you are on macos, ARM based CPU, you might need to run it as follows:
docker buildx build --platform linux/amd64 . -t nhutton/flask_test_app:0.9 -f ./Dockerfile
docker buildx build --platform linux/amd64 . -t nhutton/scraper_test_app:0.9 -f ./Dockerfile

# deploy the helmchart
helm install --set db.username=testuser,db.password=user@123,flaskImage.imagePullPolicy=Never,scraperImage.imagePullPolicy=Never flaskapptst helmcharts/

# check status
minikube status
kubectl get pods

# Expose the api to use locally (should open browser window)
minikube service flask-web-svc
# or, for a static port:
kubectl port-forward svc/flask-web-svc 8080:5000

# To update the helm chart with new docker images
helm upgrade flaskapptst helmcharts/

# To delete the storage across sessions (if really desired)
minikube ssh
# Find and remove mysql files, e.g:
ls /tmp/hostpath-provisioner/default/mysql-persistent-storage-mysql-0/
```

## To deploy to cloud (google cloud):

to be written...
