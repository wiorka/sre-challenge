# Docker

> [!NOTE] 
> This readme uses `warpnet-challenge:0.1.0` throughout as an example name of the docker image.
> Replace with your image's name and version before copy-pasting instructions.

Build and run docker image:

```bash
docker build -t warpnet-challenge:0.1.0 . 
```

```bash
docker run --rm -it -p 8000:8000 warpnet-challenge:0.1.0
```

# Minikube
## Deployment
Load required docker images into minikube and verify whether the images are present:
```bash
minikube image load warpnet-challenge:0.1.0
minikube image ls
```

Generate a secret key for the flask app and export it as an env variable. You can use `uuid` or
anything else that will generate a random string:
```bash
export FLASK_SECRET_KEY=$(cat /proc/sys/kernel/random/uuid)
```
Create a kubernetes secret that saves this key in the cluster:
```bash
kubectl create secret generic flask-secret-key --from-literal=FLASK_SECRET_KEY=${FLASK_SECRET_KEY}
```
Apply kubernets config:
```bash
kubectl apply -f kube/deployment.yaml
```
Open minikube tunnel to access the service
```bash
minikube tunnel
```
Check the IP in the load balancer details under `external IP`. Alternatively, port forward via k9s
to connect to a particular pod.

# Improvements
- The database shouldn't be included in the container, but mounted as a volume at the very least.
  Normally it would run as a separate service.
- Passwords in the database should be encrypted.
- It's recommended to put ingress in front of gunicorn to handle traffic properly.
- Reorganize the source files so it's easier to copy/mount only the required files
- Set up dependabot config
