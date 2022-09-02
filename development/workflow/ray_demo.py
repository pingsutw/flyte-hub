import typing

import ray
from flytekit import Resources, task, workflow
from flytekitplugins.ray import HeadNodeConfig, RayJobConfig, WorkerNodeConfig


@ray.remote
def f(x):
    return x * x


ray_config = RayJobConfig(
    head_node_config=HeadNodeConfig(ray_start_params={}),
    worker_node_config=[WorkerNodeConfig(group_name="test-group", replicas=1)],
    runtime_env={"pip": ["numpy", "pandas"]},
)


@task(task_config=ray_config, limits=Resources(mem="2000Mi", cpu="2"))
def ray_task() -> typing.List[int]:
    futures = [f.remote(i) for i in range(5)]
    return ray.get(futures)


@task
def t1(l: typing.List[int]) -> typing.List[int]:
    print(l)
    return l


@workflow
def wf() -> typing.List[int]:
    return t1(l=ray_task())


if __name__ == "__main__":
    print(wf())
