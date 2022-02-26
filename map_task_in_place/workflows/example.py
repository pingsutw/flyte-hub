import typing

from flytekit import task, workflow
from flytekitplugins.awsbatch import AWSBatchConfig

config = AWSBatchConfig(
    schedulingPriority=1,
    platformCapabilities="EC2",
    propagateTags=True,
    tags={"hello": "world"},
)


@task(task_config=AWSBatchConfig(schedulingPriority=1))
def t1(a: typing.List[int]) -> str:
    return str(a[0])


@task(task_config=config)
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
