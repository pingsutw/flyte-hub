import json
import os
import random
import subprocess
import time
import typing
from uuid import UUID

import flytekit.remote
from flytekit import SecurityContext
from flytekit.clis.sdk_in_container.run import get_entities_in_file, load_naive_entity
from flytekit.configuration import Config, Image, ImageConfig, SerializationSettings
from flytekit.models.security import Identity
from flytekit.remote import FlyteRemote
from flytekit.tools.translator import Options

IMAGE_NAME = "pingsutw/flyte-app"
CHECKPOINT = "checkpoints.json"
FLYTE_CONFIG = "/Users/kevin/.flyte/config-remote.yaml"
PROJECT = "flytesnacks"
DOMAIN = "development"
SERVICE_ACCOUNT = "default"
DOCKER_FILE = "Dockerfile"


def run_all_dev_workflow():
    dev_dir = "development/workflow/"
    for file in os.listdir(dev_dir):
        file_name = dev_dir + file
        rel_path = os.path.relpath(file_name)
        entities = get_entities_in_file(file_name)
        for wf in entities.workflows:
            module = os.path.splitext(rel_path)[0].replace(os.path.sep, ".")
            exe_entity = load_naive_entity(module, wf)
            print(f"Running workflow [{module}.{wf}]")
            register_and_create_wf(fn=exe_entity, input={})


def register_and_create_wf(
    fn, input: typing.Dict, rebuild_docker: bool = False, cached_image: bool = False
):
    start = time.time()

    remote, ss = create_flyte_remote(
        rebuild_docker=rebuild_docker, cached_image=cached_image
    )
    remote.register_workflow(fn, ss)
    options = Options(
        security_context=SecurityContext(
            run_as=Identity(k8s_service_account=SERVICE_ACCOUNT)
        )
    )
    remote.execute(fn, inputs=input, wait=False, options=options)

    end = time.time()
    print("Time Spend:", end - start)


def fast_register_and_create_wf(
    fn, input: typing.Dict, rebuild_docker: bool = False, cached_image: bool = False
):
    start = time.time()
    remote, ss = create_flyte_remote(
        rebuild_docker=rebuild_docker, cached_image=cached_image
    )
    version = read_version()
    options = Options(
        security_context=SecurityContext(
            run_as=Identity(k8s_service_account=SERVICE_ACCOUNT)
        )
    )
    remote_entity = remote.register_script(
        fn,
        project=PROJECT,
        domain=DOMAIN,
        options=options,
        image_config=ImageConfig(
            default_image=Image(name="default", fqn=IMAGE_NAME, tag=version)
        ),
        source_path=".",
        module_name="integration.workflow.databricks",
    )
    remote.execute(remote_entity, inputs=input, wait=False)

    end = time.time()
    print("Time Spend:", end - start)


def create_flyte_remote(
    rebuild_docker: bool = False,
    cached_image: bool = False,
    config: str = FLYTE_CONFIG,
) -> (flytekit.remote.FlyteRemote, SerializationSettings):

    version = UUID(int=random.getrandbits(128)).hex

    if rebuild_docker is True:
        _, err = build_image(IMAGE_NAME, version, cached_image)
        if err:
            raise Exception("Failed to build the image")
        push_image(IMAGE_NAME, version)
        log_version(version)
    else:
        # Ignore building docker image, and use version in checkpoint
        version = read_version()

    return (
        FlyteRemote(
            config=Config.auto(config),
            default_project=PROJECT,
            default_domain=DOMAIN,
        ),
        SerializationSettings(
            image_config=ImageConfig(
                default_image=Image(name="default", fqn=IMAGE_NAME, tag=version)
            ),
            version=version,
        ),
    )


def build_image(
    image_name: str, version: str, cache: bool = False, python_version: str = "3.9"
) -> (str, str):
    bashCommand = f"docker build . -f ./docker-image/{DOCKER_FILE} --tag {image_name}:{version} --build-arg PYTHON_VERSION={python_version}"
    if not cache:
        bashCommand = bashCommand + " --no-cache"
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
