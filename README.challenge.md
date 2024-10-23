# Build and deploy example flask application

> [!NOTE] 
> The instructions use `warpnet-challenge:0.1.0` throughout as an example name of the docker image.
> Replace with your image's name and version before copy-pasting instructions.

## Docker
### Prerequisites
 - docker

### Deployment
Build and run docker image:

```bash
docker build -t warpnet-challenge:0.1.0 . 
```
Run the image exposing the desired port:
```bash
docker run --rm -p 8000:8000 warpnet-challenge:0.1.0
```
Connect to the app via browser on `0.0.0.0:8000`.

## Kubernetes
This deployment uses minikube cluster with docker containers.

### Prerequisites
- docker
- minikube
- kubectl
- k9s (recommended)

### Deployment
Start the cluster:
```bash
minikube start
```

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

Open minikube tunnel to access the service:
```bash
minikube tunnel
```

Check the IP in the load balancer details under `external IP`:
```bash
kubectl get svc warpnet-service
```

Alternatively, port forward via k9s to connect to a particular pod.

## VM
This deployment uses Vagrant to create a VM, which is then provisioned by ansible.

### Prerequisites:
- vagrant
- ansible 

### Deployment
Vagrant installation on Fedora installs `libvirt` as a dependency, so it can be directly used
as a provider.\
Start the libvirt service, if not already running:
```bash
sudo systemctl start libvirtd
```
Install ansible collections manually, because vagrant is not great about that:
```bash
ansible-galaxy collection install -r vrequirements.yaml
```
Navigate to the `vm` folder and start the vagrant machine with provisioning:
```bash
vagrant up --provision
```
Re-provision every time the playbook changes:
```bash
vagrant provision
```

Connect to the app via `http://127.0.0.1:8000`.

# Improvements
- The database shouldn't be included in the container, but mounted as a volume at the very least.
  Normally it would run as a separate service.
- Passwords in the database should be encrypted.
- It's recommended to put nginx in front of gunicorn to handle traffic properly.
- Reorganize the source files so it's easier to copy/mount only the required files.
- Set up dependabot config.
- Set up ingress + TLS certificates in the cluster (ingress-nginx controller).
