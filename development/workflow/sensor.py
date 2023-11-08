from flytekit import task, workflow
from flytekit.sensor.file_sensor import FileSensor

sensor = FileSensor(name="test_sensor")


@task()
def t1():
    print("flyte")


@workflow
def wf(path: str = "/tmp/123"):
    sensor(path=path) >> t1()


if __name__ == "__main__":
    wf()
