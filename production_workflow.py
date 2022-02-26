import time
from typing import cast

from flytekit.remote import FlyteWorkflow, FlyteWorkflowExecution

import benchmark.workflows.map_task
import chain_tasks.workflows.example
import dataclass.workflows.example
import dynamic.workflows.example

# import flyte_pickle.workflows.example
import flytetype_in_dataclass.workflows.example
import long_list.workflows.example
import map_task.workflows.example
import map_task_in_place.workflows.example
import myapp.workflows.example
import named_tuple.workflows.example
import snowflake.workflows.example
import structured_dataset.workflows.example
import subworkflow.workflows.example
from constants import FlyteCluster
from utils import create_flyte_remote

start = time.time()

remote, version = create_flyte_remote(
    fast=True, cached_image=False, url=FlyteCluster.local
)
# Benchmark tests
# remote.execute(benchmark.workflows.map_task.my_map_workflow, inputs={"a": 10}, version=version, wait=False)

# remote.execute(chain_tasks.workflows.example.chain_tasks_wf, inputs={}, version=version, wait=True)
# remote.execute(dataclass.workflows.example.base_wf, inputs={"path": "/tmp/hello.txt"}, version=version, wait=False)
# remote.execute(dynamic.workflows.example.wf, inputs={"s1": "hello", "s2": "kevin"}, version=version, wait=False)
# remote.execute(flyte_pickle.workflows.example.welcome, inputs={"name": "Kevin"}, version=version, wait=False)
# remote.execute(flytetype_in_dataclass.workflows.example.base_wf, inputs={}, version=version, wait=False)
# remote.execute(long_list.workflows.example.my_wf, inputs={"n": 2}, version=version, wait=False)
# remote.execute(map_task1.workflows-.example.my_map_workflow, inputs={"a": 3}, version=version, wait=False)
# remote.execute(map_task_in_place.workflows.example.my_wf, inputs={"a": 2, "b": "hello"}, version=version, wait=False)
# remote.execute(myapp.workflows.example.my_wf, inputs={}, version=version, wait=True)
# res = remote.fetch_workflow_execution(name="z4wqw6alwd")
# remote.execute(named_tuple.workflows.example.my_wf, inputs={"a": 3, "b": "2"}, version=version, wait=True)
# remote.execute(snowflake.workflows.example.no_io_wf, inputs={}, wait=False)
remote.execute(structured_dataset.workflows.example.wf, inputs={}, wait=False)
# remote.execute(subworkflow.workflows.example.parent_wf, inputs={"a": 3}, version=version, wait=False)
# remote.fetch_workflow_execution(project="flytesnacks", domain="development", name="f8cd9a3bcf3024e67acf")

# print(res)
# print(res.output)
end = time.time()
print("Time Spend:", end - start)
