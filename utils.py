import json
import random
import subprocess
import time
from uuid import UUID

import flytekit.remote
from flytekit.configuration import (
    Config,
    Image,
    ImageConfig,
    PlatformConfig,
    SerializationSettings,
)
from flytekit.remote import FlyteRemote

IMAGE_NAME = "pingsutw/flyte-app"
CHECKPOINT = "checkpoints.json"


def register_and_create_wf(fn):
    start = time.time()

    remote, ss = create_flyte_remote(fast=False, cached_image=False)
    remote.register_workflow(fn, ss)
    remote.execute(fn, inputs={}, wait=False)

    end = time.time()
    print("Time Spend:", end - start)


def create_flyte_remote(
    fast: bool = False,
    cached_image: bool = False,
    config: str = "/Users/kevin/.flyte/config.yaml",
) -> (flytekit.remote.FlyteRemote, SerializationSettings):

    version = UUID(int=random.getrandbits(128)).hex

    if fast is False:
        _, err = build_image(IMAGE_NAME, version, cached_image)
        push_image(IMAGE_NAME, version)
        log_version(version)
    else:
        # Ignore building docker image, and use version in checkpoint
        version = read_version()

    return (
        FlyteRemote(
            config=Config.auto(config),
            default_project="flytesnacks",
            default_domain="development",
        ),
        SerializationSettings(
            image_config=ImageConfig(
                default_image=Image(name="default", fqn=IMAGE_NAME, tag=version)
            ),
            version=version,
        ),
    )


def build_image(
    image_name: str, version: str, cache: bool = False, base_image: str = "python3.8"
) -> (str, str):
    bashCommand = f"docker build . -f ./docker-image/Dockerfile --tag {image_name}:{version} --build-arg BASE_IMAGE_VERSION={base_image} --no-cache"
    if cache:
        bashCommand = f"docker build . -f ./docker-image/Dockerfile --tag {image_name}:{version} --build-arg BASE_IMAGE_VERSION={base_image}"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    return process.communicate()


def push_image(image_name: str, version: str):
    bashCommand = f"docker push {image_name}:{version}"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    process.communicate()


def log_version(version: str):
    with open(CHECKPOINT, "r") as jsonfile:
        checkpoints = json.load(jsonfile)
        checkpoints["image_version"] = version
        with open(CHECKPOINT, "w") as output_file:
            output_file.write(json.dumps(checkpoints))


def read_version() -> str:
    with open(CHECKPOINT, "r") as json_file:
        return json.load(json_file)["image_version"]
