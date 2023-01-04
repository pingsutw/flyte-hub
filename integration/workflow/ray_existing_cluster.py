import typing

import ray
from flytekit import task, workflow


@ray.remote
def f(x):
    return x * x


@task()
def ray_task() -> typing.List[int]:
    ray.init(address="xqpxjbschrmb6glg8rx-n0-0-raycluster-mx97k-head-svc:10001")
    futures = [f.remote(i) for i in range(5)]
    return ray.get(futures)


@workflow
def wf() -> typing.List[int]:
    return ray_task()


if __name__ == "__main__":
    print(wf())
