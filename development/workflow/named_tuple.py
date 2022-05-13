import typing

from flytekit import LaunchPlan, task, workflow


@task
def t1(a: int) -> typing.NamedTuple("OutputsBC", t1_int_output=int, c=str):
    return a + 2, "world"


@task
def t2(a: str, b: str) -> str:
    return b + a


# %%
# You can treat the outputs of a task as you normally would a Python function. Assign the output to two variables
# and use them in subsequent tasks as normal. See :py:func:`flytekit.workflow`
@workflow
def my_wf(a: int = 3, b: str = "hello") -> (int, str):
    x, y = t1(a=a)
    d = t2(a=y, b=b)
    return x, d
