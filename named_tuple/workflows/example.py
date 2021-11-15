import typing

from flytekit import task, workflow, LaunchPlan


@task
def t1(a: int) -> typing.NamedTuple("OutputsBC", t1_int_output=int, c=str):
    return a + 2, "world"


@task
def t2(a: str, b: str) -> str:
    return b + a


# %%
# You can treat the outputs of a task as you normally would a Python function. Assign the output to two variables
# and use them in subsequent tasks as normal. See :py:func:`flytekit.workflow`
@workflow
def my_wf(a: int, b: str) -> (int, str):
    x, y = t1(a=a)
    d = t2(a=y, b=b)
    return x, d


# %%
# Execute the Workflow, simply by invoking it like a function and passing in
# the necessary parameters
#
# .. note::
#
#   One thing to remember, currently we only support ``Keyword arguments``. So
#   every argument should be passed in the form ``arg=value``. Failure to do so
#   will result in an error

from flytekit.core import context_manager
from flytekit.core.context_manager import ImageConfig, Image
from flytekit.remote import FlyteRemote


remote = FlyteRemote(flyte_admin_url="localhost:30081",
                    insecure=True,
                    default_project="flyteexamples",
                    default_domain="development",
                    image_config=ImageConfig(default_image=Image(name='default', fqn='pingsutw/nt', tag='latest4'), images=[]))

#remote.register(t1, version=VERSION, name="named_tuple.workflows.example.t1")
#remote.register(t2, version=VERSION, name="named_tuple.workflows.example.t2")
# remote.register(my_wf, version=VERSION, name="named_tuple.workflows.example.t2")
if __name__ == "__main__":
    module_name="named_tuple.workflows.example"
    
    VERSION="v12"
    remote.register(t1, version=VERSION, name="named_tuple.workflows.example.t1", task_module=module_name)
    remote.register(t2, version=VERSION, name="named_tuple.workflows.example.t2", task_module=module_name)
    remote.register(my_wf, version=VERSION, name="named_tuple.workflows.example.my_wf")
    ctx = context_manager.FlyteContext.current_context()
    my_wf.name="named_tuple.workflows.example.my_wf"
    default_lp = LaunchPlan.get_default_launch_plan(ctx, my_wf)
    remote.register(default_lp, version=VERSION)
    remote.execute(my_wf, version=VERSION, inputs={"a":1, "b": "2"}, wait=True)

# t1.name = "named_tuple.workflows.example.t1"
# t2.name = "named_tuple.workflows.example.t2"
# my_wf.name = "named_tuple.workflows.example.my_wf"

# remote.register(t1, version=VERSION)
# remote.register(t2, version=VERSION)
# remote.register(my_wf, version=VERSION)

# ctx = context_manager.FlyteContext.current_context()
# default_lp = LaunchPlan.get_default_launch_plan(ctx, my_wf)
# remote.register(default_lp, version=VERSION)


# if __name__ == "__main__":
#    print(f"Running my_wf(a=50, b='hello') {my_wf(a=50, b='hello')}")

