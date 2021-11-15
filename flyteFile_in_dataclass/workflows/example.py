from dataclasses import dataclass

from dataclasses_json import dataclass_json

from flytekit import task, workflow
from flytekit.types.file import FlyteFile


@dataclass_json
@dataclass
class InnerFileStruct(object):
    a: FlyteFile


@dataclass_json
@dataclass
class FileStruct(object):
    a: FlyteFile
    b: InnerFileStruct

@task
def creat_file(path: str) -> FileStruct:
    with open(path, "w") as w:
        w.write("Hello World\n")
    file = FlyteFile(path)
    fs = FileStruct(a=file, b=InnerFileStruct(a=file))
    return fs

@task
def get_file_path(fs: FileStruct) -> str:
    return fs.a.path

@workflow
def base_wf(path: str) -> str:
    n1 = creat_file(path=path)
    return get_file_path(fs=n1)


if __name__ == "__main__":
    print("Flyte File in dataclass")
    base_wf(path="/tmp/hello.txt")


