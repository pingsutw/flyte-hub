import pandas as pd

from dataclasses import dataclass
from dataclasses_json import dataclass_json
from flytekit import kwtypes, task, workflow
from flytekit.types.schema import FlyteSchema

SomeSchema = FlyteSchema[kwtypes(some_str=str)]


@dataclass_json
@dataclass
class SomeResult:
    some_int: int
    some_schema: SomeSchema


@task
def some_task() -> SomeResult:
    some_schema = SomeSchema()
    print("some_schema", some_schema.local_path)
    some_df = pd.DataFrame(data={"some_str": ["a", "b", "c"]})
    some_schema.open().write(some_df)

    return SomeResult(some_int=1, some_schema=some_schema)


@workflow
def some_workflow() -> SomeResult:
    return some_task()

some_workflow()
