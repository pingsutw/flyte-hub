import typing
from typing import List

from flytekit import ContainerTask, kwtypes, map_task, task, workflow

calculate_ellipse_area_shell = ContainerTask(
    name="ellipse-area-metadata-python",
    input_data_dir="/var/inputs",
    output_data_dir="/var/outputs",
    inputs=kwtypes(a=int),
    outputs=kwtypes(area=float),
    image="pingsutw/raw-container:v9",
    command=[
        "python",
        "test.py",
        "{{.inputs.a}}",
        "/var/outputs",
    ],
)


@task
def coalesce(b: List[str]) -> str:
    coalesced = "".join(b)
    return coalesced


@task
def g_l(n: int) -> List[int]:
    res = []
    for i in range(n):
        res.append(i)
    return res


@workflow
def wf(n: int = 2):
    l = g_l(n=n)
    map_task(calculate_ellipse_area_shell)(a=l)


if __name__ == "__main__":
    result = wf()
