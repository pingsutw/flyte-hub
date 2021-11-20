import typing

from flytekit import task, workflow


@task
def t0(a: int) -> typing.Union[int, str]:
    return a


@task
def t1(a: typing.Union[int, str]) -> typing.Union[int, str]:
    return a


@workflow
def wf(a: int) -> typing.Union[int, str]:
    r = t0(a=a)
    return t1(a=r)


if __name__ == "__main__":
    print(f"Running my_wf() {wf(a=500)}")

