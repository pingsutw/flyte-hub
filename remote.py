import typing
import uuid

from mock import mock

from flytekit.common.exceptions.user import FlyteEntityAlreadyExistsException, FlyteEntityNotExistException
from flytekit.core import context_manager
from flytekit.core.context_manager import ImageConfig, Image
from flytekit.remote import FlyteRemote
from flytekit import task, workflow, LaunchPlan
from flytekit.core import context_manager

remote = FlyteRemote(flyte_admin_url="localhost:30081",
                    insecure=True,
                    default_project="flyteexamples",
                    default_domain="development",
                    image_config=ImageConfig(default_image=Image(name='default', fqn='pingsutw/myapp', tag='dataclass'), images=[]))


VERSION = "v2"
from dataclass.workflows.example import base_wf
from dataclass.workflows.example import get_file_path
from dataclass.workflows.example import creat_file

remote.register(creat_file, version=VERSION)
remote.register(get_file_path, version=VERSION)
remote.register(base_wf, version=VERSION)

ctx = context_manager.FlyteContext.current_context()
default_lp = LaunchPlan.get_default_launch_plan(ctx, base_wf)
remote.register(default_lp, version=VERSION)


exe = remote.execute(base_wf, inputs={"path": "/tmp/hello.txt"}, version=VERSION, wait=False)

