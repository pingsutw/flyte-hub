import typing

from flytekit import task, workflow


@task
def t0(a: int) -> typing.Union[int, str]:
    return a


@task
def t1(a: typing.Union[int, str]) -> typing.Union[int, str]:
    return a


@workflow
def union_wf(a: int = 3) -> typing.Union[int, str]:
    r = t0(a=a)
    return t1(a=r)


if __name__ == "__main__":
    print(f"Running my_wf() {union_wf(a=500)}")
