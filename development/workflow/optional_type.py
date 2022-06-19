import typing

from flytekit import task, workflow

hello_output = typing.NamedTuple("OP", greet=str)


@task()
def say_hello(a: typing.Optional[int]) -> typing.Optional[int]:
    return a


@task
def say_hello1(a: typing.Optional[int]) -> typing.Optional[int]:
    return a


@workflow()
def wf(a: int = 2) -> typing.Optional[int]:
    r = say_hello(a=a)
    return say_hello1(a=r)


if __name__ == "__main__":
    print(f"Running my_wf() {wf(a=3)}")
