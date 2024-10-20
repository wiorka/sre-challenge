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

Load required docker images into minikube and verify whether the images are present:
```
minikube image load warpnet-challenge:0.1.0
minikube image ls
```

# Improvements
- The database shouldn't be included in the container, but mounted as a volume at the very least.
  Normally it would run as a separate service.
- Passwords in the database should be encrypted.
- It's recommended to put ingress in front of gunicorn to handle traffic properly.
- Reorganize the source files so it's easier to copy/mount only the required files
- Set up dependabot config
