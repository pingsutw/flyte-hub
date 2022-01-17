import json
import random
import subprocess
from uuid import UUID

import flytekit.remote
from flytekit.core.context_manager import Image, ImageConfig
from flytekit.remote import FlyteRemote

from constants import FlyteCluster


def create_flyte_remote(
    fast: bool = False, cached_image: bool = False, url: FlyteCluster = FlyteCluster.local,
) -> (flytekit.remote.FlyteRemote, str):
    image_name = "pingsutw/flyte-app"
    version = UUID(int=random.getrandbits(128)).hex

    if fast is False:
        build_image(image_name, version, cached_image)
        push_image(image_name, version)
        log_version(version)
    else:
        # Ignore building docker image, and use version in checkpoint
        version = read_version()

    return FlyteRemote(
        flyte_admin_url=url.value,
        insecure=True,
        default_project="flyteexamples",
        default_domain="development",
        image_config=ImageConfig(
            default_image=Image(name="default", fqn=image_name, tag=version)
        )
    ), version


def build_image(
    image_name: str, version: str, cache: bool = False, base_image: str = "python3.8"
):
    bashCommand = f"docker build . -f ./docker-image/Dockerfile --tag {image_name}:{version} --build-arg BASE_IMAGE_VERSION={base_image} --no-cache"
    if cache:
        bashCommand = f"docker build . -f ./docker-image/Dockerfile --tag {image_name}:{version} --build-arg BASE_IMAGE_VERSION={base_image}"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()


def push_image(image_name: str, version: str):
    bashCommand = f"docker push {image_name}:{version}"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    process.communicate()


def log_version(version: str):
    with open("checkpoints.json", "r") as jsonfile:
        checkpoints = json.load(jsonfile)
        checkpoints["image_version"] = version
        with open("checkpoints.json", "w") as output_file:
            output_file.write(json.dumps(checkpoints))


def read_version() -> str:
    with open("checkpoints.json", "r") as json_file:
        return json.load(json_file)["image_version"]
