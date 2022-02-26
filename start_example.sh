#!/bin/bash

set -e

REGISTRY='pingsutw'
BASE_IMAGE_VERSION='python3.8'
IMAGE='flyte-app'
APP_NAME="" # image tag
VERSION='v1' # workflow, task version

while getopts a:r:v:h flag
do
    case "${flag}" in
        a) APP_NAME=${OPTARG};;
        r) REGISTRY=${OPTARG};;
        v) VERSION=${OPTARG};;
        b) VERSION=${BASE_IMAGE_VERSION};;
        h) echo "Usage: ${0} [-h|[-a <app_name>][-r <registry_name>][-v <version>]]"
           echo "  h: help (this message)"
           echo "  a = APP_NAME or the REPOSITORY APP_NAME. Defaults to myapp."
           echo "  r = REGISTRY name where the docker container should be pushed. Defaults to none - localhost"
           echo "  v = VERSION of the build. Defaults to using the current git head SHA"
           echo "  b = BASE_IMAGE_VERSION of the build (python3.7~python3.10, spark). Defaults to using the python3.8."
           exit 1;;
        *) echo "Usage: ${0} [-h|[-a <app_name>][-r <registry_name>][-v <version>]]"
           exit 1;;
    esac
done

if [ -z ${APP_NAME} ]; then
  echo "Please enter an APP_NAME."
fi


IMAGE_NAME="${REGISTRY}/${IMAGE}-${BASE_IMAGE_VERSION}:${APP_NAME}-${VERSION}"

start_example () {
  docker build . -f docker-image/Dockerfile --tag "${IMAGE_NAME}" # --no-cache
  docker push ${IMAGE_NAME}
  pyflyte --pkgs ${APP_NAME} package --image ${IMAGE_NAME} --force
  flytectl register files --project flyteexamples --domain development --archive flyte-package.tgz --version ${VERSION} --config ~/.flyte/config-sandbox.yaml
}

start_example
