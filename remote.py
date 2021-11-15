from flytekit.core.context_manager import ImageConfig, Image
from flytekit.remote import FlyteRemote

# import workflow
import dataclass.workflows.example
import flyte_pickle.workflows.example
import myapp.workflows.example
import named_tuple.workflows.example


remote = FlyteRemote(flyte_admin_url="kevin.io:30081",
                     insecure=True,
                     default_project="flyteexamples",
                     default_domain="development",
                     image_config=ImageConfig(default_image=Image(name='default', fqn='pingsutw/myapp', tag='myapp-v2')))

VERSION = "v2"
remote.execute(dataclass.workflows.example.base_wf, inputs={"path": "/tmp/hello.txt"}, version=VERSION, wait=False)
remote.execute(flyte_pickle.workflows.example.welcome, inputs={"name": "Kevin"}, version=VERSION, wait=False)
remote.execute(myapp.workflows.example.my_wf, inputs={}, version=VERSION, wait=False)
remote.execute(named_tuple.workflows.example.my_wf, inputs={"a": 3, "b": "2"}, version=VERSION, wait=False)
