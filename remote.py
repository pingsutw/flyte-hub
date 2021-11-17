from flytekit.core.context_manager import ImageConfig, Image
from flytekit.remote import FlyteRemote

# import workflow
import chain_tasks.workflows.example
import conditional.workflows.example
import dataclass.workflows.example
import dynamic.workflows.example
import flyte_pickle.workflows.example
import long_list.workflows.example
import map_task.workflows.example
import myapp.workflows.example
import named_tuple.workflows.example
import subworkflow.workflows.example

VERSION = "all-v4"
remote = FlyteRemote(flyte_admin_url="kevin.io:30081",
                     insecure=True,
                     default_project="flyteexamples",
                     default_domain="development",
                     image_config=ImageConfig(default_image=Image(name='default', fqn='pingsutw/all', tag=VERSION)))


remote.execute(chain_tasks.workflows.example.chain_tasks_wf, inputs={}, version=VERSION, wait=False)
# remote.execute(conditional.workflows.example.multiplier, inputs={"my_input", 3.0}, version=VERSION, wait=False)
remote.execute(dataclass.workflows.example.base_wf, inputs={"path": "/tmp/hello.txt"}, version=VERSION, wait=False)
remote.execute(dynamic.workflows.example.wf, inputs={"s1": "hello", "s2": "kevin"}, version=VERSION, wait=False)
remote.execute(flyte_pickle.workflows.example.welcome, inputs={"name": "Kevin"}, version=VERSION, wait=False)
remote.execute(long_list.workflows.example.my_wf, inputs={"n": 5}, version=VERSION, wait=False)
remote.execute(map_task.workflows.example.my_map_workflow, inputs={"a": 10}, version=VERSION, wait=False)
remote.execute(myapp.workflows.example.my_wf, inputs={}, version=VERSION, wait=False)
remote.execute(named_tuple.workflows.example.my_wf, inputs={"a": 3, "b": "2"}, version=VERSION, wait=False)
remote.execute(subworkflow.workflows.example.parent_wf, inputs={"a": 3}, version=VERSION, wait=False)
