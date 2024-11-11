# Check if there are any uncommitted changes
if [[ -n $(git status --porcelain) ]]; then
  echo "Error: There are uncommitted changes. Please commit your changes before running this script."
  exit 1
fi

TAG=$(git rev-parse --short HEAD)
# Information about Docker registry and image
REGISTRY_URL="host:port"
IMAGE_NAME="image"

# Build image Docker without cache
docker build -t $IMAGE_NAME .

# Attach image with tag (full tag)
docker tag $IMAGE_NAME:latest $REGISTRY_URL/$IMAGE_NAME:"$TAG"

# Push image to registry with tag
docker push $REGISTRY_URL/$IMAGE_NAME:"$TAG"

# Attach image with tag -latest
docker tag $IMAGE_NAME $REGISTRY_URL/$IMAGE_NAME:latest

# Push image to registry with tag 'latest'
docker push $REGISTRY_URL/$IMAGE_NAME:latest

# Remove image local
docker rmi $IMAGE_NAME