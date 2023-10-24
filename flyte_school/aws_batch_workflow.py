from flytekit import task, workflow, ImageSpec, Resources
from flytekitplugins.awsbatch import AWSBatchConfig

new_flytekit = "git+https://github.com/flyteorg/flytekit.git@master"
aws_batch = "git+https://github.com/flyteorg/flytekit.git@master#subdirectory=plugins/flytekit-aws-batch"
image = ImageSpec(apt_packages=["git"], packages=[aws_batch], registry="pingsutw")


@task(container_image=image,
      task_config=AWSBatchConfig(platformCapabilities="EC2", tags={"hello": "world"}),
      requests=Resources(cpu="1", mem="1Gi"),
      limits=Resources(cpu="1", mem="1Gi"))
def t1(a: int) -> int:
    print("t1", a)
    return a


def t2(a: int) -> int:
    print("t2", a)
    return a


@workflow
def wf(a: int = 3) -> int:
    t1(a=a)
    return t2(a=a)


if __name__ == "__main__":
    print(f"Running my_wf(a=50, b='hello') {wf(a=50)}")
