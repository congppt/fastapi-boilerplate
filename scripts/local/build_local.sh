if [ -z "$ENV_CHOICE" ]; then
    echo "Choose the environment to build image:"
    echo "1) Development"
    echo "2) Production"
    read -r -p "Enter the number corresponding to the environment (default is 1 - Development): " ENV_CHOICE
fi

if [ "$ENV_CHOICE" == 2 ]; then
    echo "You selected Production environment."
    IMAGE_NAME="mecommerce_be"
else
    echo "You selected Development environment (default)."
    IMAGE_NAME="mecommerce_be_test"
fi

# build image
docker build -t $IMAGE_NAME .
# save image to file tar
docker save -o $IMAGE_NAME.tar $IMAGE_NAME