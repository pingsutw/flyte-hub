from development.workflow.optional_type import wf
from utils import (
    create_flyte_remote,
    fast_register_and_create_wf,
    register_and_create_wf,
    run_all_dev_workflow,
)

# register_and_create_wf(wf, input={}, rebuild_docker=False)
fast_register_and_create_wf(wf, input={}, rebuild_docker=False)
