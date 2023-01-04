import typing

from flytekit import Resources, task, workflow
from flytekitplugins.awsbatch import AWSBatchConfig

config = AWSBatchConfig(
    schedulingPriority=1,
    platformCapabilities="EC2",
    propagateTags=True,
    tags={"hello": "world"},
)


@task(
    task_config=AWSBatchConfig(schedulingPriority=1),
    timeout=60,
)
def t1(a: typing.List[int]) -> str:
    exit(1)
    return str(a[0])


@task(task_config=config)
def t3(a: str, b: str) -> str:
    return b + "".join(a)


@task(task_config=config)
def create_list(size: int) -> typing.List[int]:
    res = []
    for i in range(size):
        res.append(i)
    return res


@workflow
def wf(a: int = 3, b: str = "hello") -> str:
    l = create_list(size=a)
    y = t1(a=l)
    d = t3(a=y, b=b)
    return d


if __name__ == "__main__":
    x = wf(a=3, b="hello")
    print(f"Workflow output: {x}")
