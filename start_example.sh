#!/bin/bash

set -e

REGISTRY='pingsutw'
IMAGE='myapp'
APP_NAME="" # image tag
VERSION='v1' # workflow, task version

while getopts a:r:v:h flag
do
    case "${flag}" in
        a) APP_NAME=${OPTARG};;
        r) REGISTRY=${OPTARG};;
        v) VERSION=${OPTARG};;
        h) echo "Usage: ${0} [-h|[-a <app_name>][-r <registry_name>][-v <version>]]"
           echo "  h: help (this message)"
           echo "  a: APP_NAME or the REPOSITORY APP_NAME. Defaults to myapp."
           echo "  r = REGISTRY name where the docker container should be pushed. Defaults to none - localhost"
           echo "  v = VERSION of the build. Defaults to using the current git head SHA"
           exit 1;;
        *) echo "Usage: ${0} [-h|[-a <app_name>][-r <registry_name>][-v <version>]]"
           exit 1;;
    esac
done

if [ -z ${APP_NAME} ]; then
  echo "Please enter an APP_NAME."
fi


IMAGE_NAME="${REGISTRY}/${IMAGE}:${APP_NAME}-${VERSION}"

start_example () {
  docker build . --tag "${IMAGE_NAME}" # --no-cache
  docker push ${IMAGE_NAME}
  pyflyte --pkgs ${APP_NAME} package --image ${IMAGE_NAME} --force
  flytectl register files --project flyteexamples --domain development --archive flyte-package.tgz --version ${VERSION} --config ~/.flyte/config.yaml
}

start_example
