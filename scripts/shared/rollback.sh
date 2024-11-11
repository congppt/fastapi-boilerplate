read -r -p "Please enter the commit you want to start from: " COMMIT

TAG=""

while [[ -z "$TAG" ]]; do
    read -r -p "Please enter the commit you want to start from: " COMMIT
    if [[ -n "$COMMIT" ]]; then
        TAG="$COMMIT"
    else
        echo "TAG cannot be empty. Please enter a value."
    fi
done

export TAG
source ./start.sh
