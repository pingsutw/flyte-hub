import typing

from flytekit import TaskMetadata, map_task, task, workflow


@task
def a_mappable_task(a: int) -> str:
    inc = a + 2
    stringified = str(inc)
    return stringified


@task
def coalesce(b: typing.List[str]) -> str:
    coalesced = "".join(b)
    return coalesced


@task
def create_list(n: int) -> typing.List[int]:
    res = []
    for i in range(n):
        res.append(i)
    return res


@workflow
def my_map_workflow(a: int) -> str:
    l = create_list(n=a)
    mapped_out = map_task(a_mappable_task, metadata=TaskMetadata(retries=1))(a=l)
    coalesced = coalesce(b=mapped_out)
    return coalesced


if __name__ == "__main__":
    result = my_map_workflow(a=10)
    print(f"{result}")
