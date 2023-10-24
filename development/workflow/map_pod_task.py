from typing import List

from flytekitplugins.pod import Pod
from kubernetes.client import V1PodSpec, V1Container, V1ResourceRequirements

from flytekit import map_task, task, workflow, TaskMetadata


@task(
    task_config=Pod(
        pod_spec=V1PodSpec(
            containers=[
                V1Container(
                    name="primary",
                    resources=V1ResourceRequirements(
                        requests={"cpu": ".5", "memory": "500Mi"},
                        limits={"cpu": ".5", "memory": "500Mi"},
                    ),
                )
            ],
            init_containers=[
                V1Container(
                    image="alpine",
                    name="init",
                    command=["/bin/sh"],
                    args=["-c", 'echo "I\'m a customizable init container"'],
                    resources=V1ResourceRequirements(
                        limits={"cpu": ".5", "memory": "500Mi"},
                    ),
                )
            ],
        ),
    )
)
def map_pod_task(int_val: int) -> str:
    return str(int_val)


@task
def coalesce(list_of_strings: List[str]) -> str:
    coalesced = ", ".join(list_of_strings)
    return coalesced


@workflow
def wf(list_of_ints: List[int] = [1, 2, 3, 4, 5]) -> str:
    mapped_out = map_task(map_pod_task, metadata=TaskMetadata(retries=1))(
        int_val=list_of_ints
    )
    coalesced = coalesce(list_of_strings=mapped_out)
    return coalesced
