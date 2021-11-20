import random
import subprocess
import time
from uuid import UUID

from flytekit.core.context_manager import ImageConfig, Image, EntrypointSettings
from flytekit.remote import FlyteRemote

import chain_tasks.workflows.example
import conditional.workflows.example
import dataclass.workflows.example
import dataset.workflows.example
import dynamic.workflows.example
import flyte_pickle.workflows.example
import long_list.workflows.example
import map_task.workflows.example
import mpi_job.workflows.example
import myapp.workflows.example
import named_tuple.workflows.example
import subworkflow.workflows.example
# import union_type.workflows.example

start = time.time()

version = UUID(int=random.getrandbits(128)).hex
image_name = "pingsutw/all"

# Build and push images
bashCommand = f"docker build . --tag {image_name}:{version} --no-cache"
process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
output, error = process.communicate()


bashCommand = f"docker push {image_name}:{version}"
process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
process.communicate()


remote = FlyteRemote(flyte_admin_url="localhost:30081",
                     insecure=True,
                     default_project="flyteexamples",
                     default_domain="development",
                     image_config=ImageConfig(default_image=Image(name='default', fqn=image_name, tag=version)))

# Work in progress
# remote.execute(conditional.workflows.example.multiplier, inputs={"my_input", 3.0}, version=version, wait=False)
# remote.execute(mpi_job.workflows.example.horovod_training_wf, inputs={}, version=version, wait=False)
# remote.execute(union_type.workflows.example.wf, inputs={"a": 3}, version=version, wait=False)
remote.execute(dataset.workflows.example.wf, inputs={}, version=version, wait=False)

# remote.execute(chain_tasks.workflows.example.chain_tasks_wf, inputs={}, version=version, wait=False)
# remote.execute(dataclass.workflows.example.base_wf, inputs={"path": "/tmp/hello.txt"}, version=version, wait=False)
# remote.execute(dynamic.workflows.example.wf, inputs={"s1": "hello", "s2": "kevin"}, version=version, wait=False)
# remote.execute(flyte_pickle.workflows.example.welcome, inputs={"name": "Kevin"}, version=version, wait=False)
# remote.execute(long_list.workflows.example.my_wf, inputs={"n": 5}, version=version, wait=False)
# remote.execute(map_task.workflows.example.my_map_workflow, inputs={"a": 10}, version=version, wait=False)
# remote.execute(myapp.workflows.example.my_wf, inputs={}, version=version, wait=False)
# remote.execute(named_tuple.workflows.example.my_wf, inputs={"a": 3, "b": "2"}, version=version, wait=False)
# remote.execute(subworkflow.workflows.example.parent_wf, inputs={"a": 3}, version=version, wait=False)


end = time.time()
print("Time Spend:", end - start)
