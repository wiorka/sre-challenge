# Build and run docker image
```bash
docker build -t warpnet-challenge:<version> . 
```

```bash
docker run --rm -it -p 8000:8000 warpnet-challenge:<version>
```
The database shouldn't be included in the container, but mounted as a volume at the very least.
