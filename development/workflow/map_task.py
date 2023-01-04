from typing import List

from flytekit import Resources, map_task, task, workflow


@task
def a_mappable_task(a: int):
    inc = a + 2
    raise Exception
    stringified = str(inc)


@task
def coalesce(b: List[str]) -> str:
    coalesced = "".join(b)
    raise Exception
    return coalesced


@task
def g_l(n: int) -> List[int]:
    res = []
    for i in range(n):
        res.append(i)
    return res


@workflow
def wf(n: int = 1000) -> str:
    l = g_l(n=n)
    map_task(a_mappable_task)(a=l)
    coalesced = coalesce(b=["1", "2"])
    return coalesced


if __name__ == "__main__":
    result = wf()
