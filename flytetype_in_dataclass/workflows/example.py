import tempfile
from dataclasses import dataclass

import pandas as pd
from dataclasses_json import dataclass_json
from flytekit import task, workflow
from flytekit.types.directory import FlyteDirectory
from flytekit.types.file import FlyteFile
from flytekit.types.schema import FlyteSchema


@dataclass_json
@dataclass
class InnerFileStruct(object):
    a: FlyteFile


@dataclass_json
@dataclass
class Result:
    schema: FlyteSchema
    file: FlyteFile
    directory: FlyteDirectory


@task
def upload_result() -> Result:
    df = pd.DataFrame({"Name": ["Tom", "Joseph"], "Age": [20, 22]})
    temp_dir = tempfile.mkdtemp(prefix="flyte-")

    schema_path = temp_dir + "/schema.parquet"
    df.to_parquet(schema_path)

    file_path = tempfile.NamedTemporaryFile(delete=False)
    file_path.write(b"Hello world!")
    fs = Result(
        schema=FlyteSchema(temp_dir),
        file=FlyteFile(file_path.name),
        directory=FlyteDirectory(temp_dir),
    )
    return fs


@task
def download_result(res: Result):
    assert pd.DataFrame({"Name": ["Tom", "Joseph"], "Age": [20, 22]}).equals(
        res.schema.open().all()
    )
    res.file.download()
    res.directory.download()


@workflow
def base_wf():
    res = upload_result()
    download_result(res=res)


if __name__ == "__main__":
    print("Flyte File in dataclass")
    base_wf()
