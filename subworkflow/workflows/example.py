import typing
from typing import Tuple

from flytekit import task, workflow

op = typing.NamedTuple("OutputsBC", t1_int_output=int, c=str)


@task
def t1(a: int) -> op:
    return op(a + 2, "world")


@workflow
def my_subwf(a: int = 42) -> Tuple[str, str]:
    x, y = t1(a=a)
    u, v = t1(a=x)
    return y, v


@workflow
def parent_wf(a: int) -> Tuple[int, str, str]:
    x, y = t1(a=a).with_overrides(node_name="node-t1-parent")
    u, v = my_subwf(a=x)
    return x, u, v


if __name__ == "__main__":
    print(f"Running parent_wf(a=3) {parent_wf(a=3)}")
