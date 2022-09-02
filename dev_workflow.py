from development.workflow.test import wf
from integration.workflow.bigquery_plugin import full_bigquery_wf
from utils import (
    create_flyte_remote,
    fast_register_and_create_wf,
    register_and_create_wf,
    run_all_dev_workflow,
)

register_and_create_wf(wf, input={}, rebuild_docker=True)
