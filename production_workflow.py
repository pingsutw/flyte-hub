import benchmark.workflows.map_task
import chain_tasks.workflows.example
import dataclass.workflows.example
import dynamic.workflows.example

# import flyte_pickle.workflows.example
import flytetype_in_dataclass.workflows.example
import long_list.workflows.example
import map_task.workflows.example

# import map_task_in_place.workflows.example
import myapp.workflows.example
import named_tuple.workflows.example
import secret_demo.workflows.example

# import snowflake.workflows.example
import structured_dataset.workflows.example
import subworkflow.workflows.example
from constants import FlyteCluster
from utils import create_flyte_remote, register_and_create_wf

register_and_create_wf(subworkflow.workflows.example.parent_wf, input={"a": 3}, fast=True)
# register_and_create_wf(dynamic.workflows.example.wf, input={"s1": "hi", "s2": "hello"}, fast=True)
