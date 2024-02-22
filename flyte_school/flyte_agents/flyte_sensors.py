from flytekit import ImageSpec, task, workflow
from flytekit.sensor.file_sensor import FileSensor
from flytekitplugins.my_agent import FlyteReleaseSensor

release_sensor = FlyteReleaseSensor(name="release_sensor")
flyte_sensor = FileSensor(name="file_sensor")
image_spec = ImageSpec(
    base_image="pingsutw/flyte-school:agent-amd64",
    packages=["numpy"],
    registry="pingsutw",
)


@task(container_image=image_spec)
def t1():
    print("success!!!")


@workflow()
def file_sensor_wf(path: str):
    flyte_sensor(path=path) >> t1()


@workflow()
def release_sensor_wf(version: str):
    release_sensor(version=version) >> t1()
