from flytekit import ImageSpec, Resources, task, workflow
import ray
from flytekitplugins.ray import HeadNodeConfig, RayJobConfig, WorkerNodeConfig


custom_image = ImageSpec(
    registry="pingsutw",
    packages=["flytekitplugins-ray"],
)


ray_config = RayJobConfig(
    head_node_config=HeadNodeConfig(ray_start_params={"log-color": "False"}),
    worker_node_config=[WorkerNodeConfig(group_name="ray-group", replicas=1)],
)


@ray.remote
def f1(x):
    return x * x


@ray.remote
def f2(x):
    return x % 2


@task(requests=Resources(mem="900Mi", cpu="1"), container_image=custom_image, task_config=ray_config)
def ray_task(n: int) -> int:
    futures = [f2.remote(f1.remote(i)) for i in range(n)]
    return sum(ray.get(futures))


@workflow
def ray_workflow(n: int = 10) -> int:
    return ray_task(n=n)


if __name__ == '__main__':
    ray_workflow(n=10)
