from dataclasses import dataclass

from dataclasses_json import dataclass_json
from flytekit import task, workflow


@dataclass_json
@dataclass
class FileStruct(object):
    a: str
    b: str


@task
def creat_file(path: str) -> FileStruct:
    fs = FileStruct(a=path, b=path)
    return fs


@task
def get_file_path(fs: FileStruct) -> str:
    return fs.a


@workflow
def base_wf(path: str) -> str:
    n1 = creat_file(path=path)
    return get_file_path(fs=n1)


if __name__ == "__main__":
    print("Flyte File in dataclass")
    base_wf(path="/tmp/hello.txt")
