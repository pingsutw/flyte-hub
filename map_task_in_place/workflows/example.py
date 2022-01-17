import typing

from flytekit import TaskMetadata, map_task, task, workflow
from flytekitplugins.awsbatch import AWSBatch

config = AWSBatch(
    schedulingPriority=1,
    PlatformCapabilities=["EC2"],
    PropagateTags=True,
    RetryStrategy={"attempts": 10},
    Tags={"hello": "world"},
    Timeout={"attemptDurationSeconds": 60},
)


@task(task_config=AWSBatch(Tags={"hello": "world"}))
def t1(a: typing.List[int]) -> str:
    return str(a[0])


@task(task_config=AWSBatch(Tags={"hello": "flyte"}))
def t3(a: str, b: str) -> str:
    return b + "".join(a)


@task(task_config=config)
def create_list(n: int) -> typing.List[int]:
    res = []
    for i in range(n):
        res.append(i)
    return res


@workflow
def my_wf(a: int, b: str) -> str:
    l = create_list(n=a)
    y = t1(a=l)
    d = t3(a=y, b=b)
    return y


if __name__ == "__main__":
    x = my_wf(a=3, b="hello")
    print(f"Workflow output: {x}")
