# flyte-app

- Flyte example - contains many kind of flyte examples for new users
- Flyte benchmark - microbenchmark testing for evaluating Flyte performance

## Prerequisite
Install python dependencies
```bash
pip install -r requirements.txt
```

## Quick Start (flytekit)
```python
from utils import register_and_create_wf
from development.workflow.raw_container import wf

register_and_create_wf(wf, input={"a": 3.0, "b": 4.0}, fast=False)
```
- Output will be like
```bash
Running workflow [development.workflow.flyte_type_in_dataclass.base_wf]
Time Spend: 4.274042129516602
```