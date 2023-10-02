#!/usr/bin/env bash

# Use option --no-login to skip docker login if you already logged in Docker registry.
NO_LOGIN=$1

REGISTRY_URL="https://index.docker.io/v1/"
REGISTRY='ewproductsecurity'
IMAGE_NAME='hvss-calculator-service'
IMAGE_REPO="$REGISTRY/$IMAGE_NAME"

login() {
    if [ -z "$NO_LOGIN" ]; then
        docker_login
    fi
}

docker_login() {
    if [ -z "$DOCKER_PAT" ]
    then
        echo -e "\nPlease provide Personal Access Token (PAT) for the registry ($REGISTRY_URL): $REGISTRY"
        echo -e "\nThe PAT expected as a shell environment variable DOCKER_PAT.\nFor example:"
        echo -e "\texport DOCKER_PAT=11111\n"
        exit 1
    else
        echo "$DOCKER_PAT" | docker login $REGISTRY_URL -u $REGISTRY --password-stdin
        if [ $? -ne 0 ]; then
            echo -e "\nPlease try again.\n"
            exit 1
        fi
        unset ACCESS_TOKEN
    fi
}

show_local_images() {
    echo -e "\nLocal images in the repository '$IMAGE_NAME':"
    docker image ls | grep $IMAGE_NAME
    echo
}

build_new_image() {
    echo -e "\nBuilding new Docker container image: $IMAGE_REPO ..."
    docker build -t $IMAGE_REPO .
}

retag_new_image() {
    # TODO: Re-tag new image
    # echo "Re-tagging Docker container image to ${IMAGE_REPO}:tag ..."
    echo
}

publish_new_image() {
    # Push tag 'latest'
    echo -e "Pushing the image into Docker Hub Registry: $IMAGE_REPO ...\n"
    docker push $IMAGE_REPO

    # TODO: Push tag <some_specific_tag>
    # Get specific tag
    # TAG=<some_specific_tag>
    # echo "Pushing the image into Docker Registry: $IMAGE_REPO:$TAG ..."
}

test() {
    echo "Running Test function..."
    login
    echo "Exiting Test function..."
}

main() {
    login
    show_local_images
    build_new_image
    retag_new_image
    show_local_images
    publish_new_image
}

# Run test function
# test

# Run main function
main
