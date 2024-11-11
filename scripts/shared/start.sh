# If user doesn't enter a tag, use latest tag
if [ -z "$TAG" ]; then
  TAG="latest"
fi

export IMAGE="host:port/name:$TAG"
SERVICE="service_name"

# check if container is running
if docker-compose ps -q $SERVICE > /dev/null; then
    docker-compose stop $SERVICE
    # remove container
    docker-compose rm -f $SERVICE
fi

# check if old image is still available
if docker images -q "$IMAGE" > /dev/null; then
    # remove old image
    docker rmi "$IMAGE"
fi

# pull latest image
docker-compose pull $SERVICE
# restart service (without restarting dependencies)
docker-compose up -d --no-deps $SERVICE