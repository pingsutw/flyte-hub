from development.workflow.my_app import my_wf

# from integration.workflow.aws_batch import wf
from utils import (
    create_flyte_remote,
    fast_register_and_create_wf,
    register_and_create_wf,
    run_all_dev_workflow,
)

# Register and run a new workflow
# 1. Add a new workflow to the development directory
# 2. Update python dependency in the dockerfile
# 3. Update flyte config in util.py if needed
register_and_create_wf(my_wf, input={}, rebuild_docker=True, cached_image=True)
