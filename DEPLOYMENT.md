# Deployment Guide

This guide covers different deployment options for the Top 5 Things Email Generator.

## Table of Contents

- [Using Pre-built Docker Image (Recommended)](#using-pre-built-docker-image)
- [Building Locally](#building-locally)
- [Deployment Options](#deployment-options)
- [GitHub Container Registry](#github-container-registry)
- [Environment Configuration](#environment-configuration)

## Using Pre-built Docker Image (Recommended)

The easiest way to run the application is using the pre-built Docker image from GitHub Container Registry (GHCR).

### Prerequisites

- Docker, Colima, or Minikube installed
- Azure AD app registration completed (see SETUP.md)
- `.env` file configured

### Quick Start with GHCR Image

1. **Pull the latest image**
   ```bash
   docker pull ghcr.io/chadchappy/t5t:latest
   ```

2. **Run the container**
   ```bash
   docker run -p 5000:5000 --env-file .env ghcr.io/chadchappy/t5t:latest
   ```

3. **Or use Docker Compose**
   ```bash
   # Pull the latest image
   docker-compose pull
   
   # Start the application
   docker-compose up
   ```

### Available Image Tags

- `latest` - Latest stable build from main branch
- `main` - Latest build from main branch
- `sha-<commit>` - Specific commit builds
- `v1.0.0` - Semantic version tags (when released)

## Building Locally

If you want to build the image yourself or make modifications:

### Build with Docker

```bash
# Build the image
docker build -t top5agent .

# Run the container
docker run -p 5000:5000 --env-file .env top5agent
```

### Build with Docker Compose

```bash
# Build and start
docker-compose up --build

# Or build without starting
docker-compose build
```

### Build for Multiple Platforms

```bash
# Set up buildx
docker buildx create --use

# Build for multiple platforms
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t top5agent:latest \
  --load \
  .
```

## Deployment Options

### Option 1: Docker Desktop

**Best for:** macOS and Windows users

```bash
# Start Docker Desktop from Applications

# Pull and run
docker-compose pull
docker-compose up
```

### Option 2: Colima (macOS)

**Best for:** macOS users who prefer open-source alternative to Docker Desktop

```bash
# Install Colima
brew install colima docker docker-compose

# Start Colima
colima start --cpu 2 --memory 4

# Pull and run
docker-compose pull
docker-compose up
```

### Option 3: Minikube (Kubernetes)

**Best for:** Users who want to run in Kubernetes

#### Using Pre-built Image

```bash
# Start Minikube
minikube start

# Create namespace
kubectl create namespace top5agent

# Create secret from .env file
kubectl create secret generic top5agent-env \
  --from-env-file=.env \
  -n top5agent

# Create deployment
kubectl create deployment top5agent \
  --image=ghcr.io/chadchappy/t5t:latest \
  --port=5000 \
  -n top5agent

# Set environment from secret
kubectl set env deployment/top5agent \
  --from=secret/top5agent-env \
  -n top5agent

# Expose service
kubectl expose deployment top5agent \
  --type=NodePort \
  --port=5000 \
  -n top5agent

# Get URL
minikube service top5agent -n top5agent --url
```

#### Using Kubernetes Manifests

Create `k8s/deployment.yaml`:

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: top5agent
---
apiVersion: v1
kind: Secret
metadata:
  name: top5agent-env
  namespace: top5agent
type: Opaque
stringData:
  CLIENT_ID: "your-client-id"
  CLIENT_SECRET: "your-client-secret"
  TENANT_ID: "your-tenant-id"
  SECRET_KEY: "your-secret-key"
  REDIRECT_URI: "http://localhost:5000/callback"
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: top5agent
  namespace: top5agent
spec:
  replicas: 1
  selector:
    matchLabels:
      app: top5agent
  template:
    metadata:
      labels:
        app: top5agent
    spec:
      containers:
      - name: top5agent
        image: ghcr.io/chadchappy/t5t:latest
        ports:
        - containerPort: 5000
        envFrom:
        - secretRef:
            name: top5agent-env
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
---
apiVersion: v1
kind: Service
metadata:
  name: top5agent
  namespace: top5agent
spec:
  type: NodePort
  selector:
    app: top5agent
  ports:
  - port: 5000
    targetPort: 5000
```

Deploy:
```bash
kubectl apply -f k8s/deployment.yaml
minikube service top5agent -n top5agent --url
```

### Option 4: Podman

**Best for:** Users who prefer Podman over Docker

```bash
# Pull image
podman pull ghcr.io/chadchappy/t5t:latest

# Run container
podman run -p 5000:5000 --env-file .env ghcr.io/chadchappy/t5t:latest
```

## GitHub Container Registry

### Pulling Images

Images are automatically built and pushed to GHCR on every commit to main branch.

```bash
# Pull latest
docker pull ghcr.io/chadchappy/t5t:latest

# Pull specific version
docker pull ghcr.io/chadchappy/t5t:v1.0.0

# Pull specific commit
docker pull ghcr.io/chadchappy/t5t:sha-abc123
```

### Authentication (if repository is private)

```bash
# Create GitHub Personal Access Token with read:packages scope
# Then login:
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin
```

### Image Information

View image details:
```bash
docker inspect ghcr.io/chadchappy/t5t:latest
```

## Environment Configuration

### Required Environment Variables

All deployment methods require these environment variables:

```bash
CLIENT_ID=<your-azure-ad-client-id>
CLIENT_SECRET=<your-azure-ad-client-secret>
TENANT_ID=<your-azure-ad-tenant-id>
SECRET_KEY=<random-secret-key>
REDIRECT_URI=http://localhost:5000/callback
```

### Configuration Methods

#### Method 1: .env file (Docker Compose)

```bash
# Create .env file
cp .env.example .env
# Edit .env with your values

# Use with docker-compose
docker-compose up
```

#### Method 2: Environment variables (Docker)

```bash
docker run -p 5000:5000 \
  -e CLIENT_ID=your-client-id \
  -e CLIENT_SECRET=your-client-secret \
  -e TENANT_ID=your-tenant-id \
  -e SECRET_KEY=your-secret-key \
  -e REDIRECT_URI=http://localhost:5000/callback \
  ghcr.io/chadchappy/t5t:latest
```

#### Method 3: Kubernetes Secret

```bash
kubectl create secret generic top5agent-env \
  --from-literal=CLIENT_ID=your-client-id \
  --from-literal=CLIENT_SECRET=your-client-secret \
  --from-literal=TENANT_ID=your-tenant-id \
  --from-literal=SECRET_KEY=your-secret-key \
  --from-literal=REDIRECT_URI=http://localhost:5000/callback
```

## Health Checks

### Check if container is running

```bash
# Docker
docker ps | grep top5agent

# Kubernetes
kubectl get pods -n top5agent
```

### Check application health

```bash
# Test endpoint
curl http://localhost:5000

# Should return HTML content
```

### View logs

```bash
# Docker Compose
docker-compose logs -f

# Docker
docker logs -f <container-id>

# Kubernetes
kubectl logs -f deployment/top5agent -n top5agent
```

## Updating

### Update to latest version

```bash
# Docker Compose
docker-compose pull
docker-compose up -d

# Docker
docker pull ghcr.io/chadchappy/t5t:latest
docker stop top5agent
docker rm top5agent
docker run -p 5000:5000 --env-file .env ghcr.io/chadchappy/t5t:latest

# Kubernetes
kubectl rollout restart deployment/top5agent -n top5agent
```

## Troubleshooting

### Image pull fails

```bash
# Check if you're logged in (for private repos)
docker login ghcr.io

# Try pulling with full path
docker pull ghcr.io/chadchappy/t5t:latest
```

### Container won't start

```bash
# Check logs
docker logs <container-id>

# Verify environment variables
docker inspect <container-id> | grep -A 20 Env
```

### Port already in use

```bash
# Find what's using port 5000
lsof -i :5000

# Use different port
docker run -p 8080:5000 --env-file .env ghcr.io/chadchappy/t5t:latest
```

## Production Considerations

### Security

- Use secrets management (Kubernetes Secrets, Docker Secrets, etc.)
- Never commit `.env` file
- Rotate CLIENT_SECRET regularly
- Use HTTPS in production (add reverse proxy)

### Performance

- Allocate sufficient memory (512MB minimum, 1GB recommended)
- Use persistent volumes for session data if needed
- Consider horizontal scaling for multiple users

### Monitoring

- Set up container health checks
- Monitor resource usage
- Track application logs
- Set up alerts for failures

## Support

For deployment issues:
1. Check container logs
2. Verify environment variables
3. Ensure Azure AD app is configured correctly
4. Review SETUP.md for configuration details

