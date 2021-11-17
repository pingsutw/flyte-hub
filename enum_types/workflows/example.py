from flytekit import task, workflow
from typing import Tuple
from enum import Enum


class Color(Enum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"


@task
def enum_stringify(c: Color) -> str:
    return c.value


@task
def string_to_enum(c: str) -> Color:
    return Color(c)


@workflow
def enum_wf(c: Color = Color.RED) -> Tuple[Color, str]:
    v = enum_stringify(c=c)
    return string_to_enum(c=v), v


if __name__ == "__main__":
    print(enum_wf())
