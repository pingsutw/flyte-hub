import os
os.environ["FLYTE_SDK_LOGGING_LEVEL_ROOT"] = "40"
from utils import register_and_create_wf, run_all_dev_workflow
from development.workflow.raw_container import wf

# register_and_create_wf(wf, input={"a": 3.0, "b": 4.0}, rebuild_docker=False)
run_all_dev_workflow()
