# container to get logs
CONTAINER_NAME="name"

# check if container is running
if ! docker ps --filter "name=${CONTAINER_NAME}" | grep -q "${CONTAINER_NAME}"; then
    echo "Container ${CONTAINER_NAME} not running"
    exit 1
fi

# print logs
echo "Log container ${CONTAINER_NAME}..."
docker-compose logs -f --tail=100 ${CONTAINER_NAME}
