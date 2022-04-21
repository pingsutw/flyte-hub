from flytekit import task, workflow


@task
def say_hello1() -> int:
    return 1


@workflow
def my_wf() -> int:
    res = say_hello1()
    print(res)
    return res


if __name__ == "__main__":
    print(f"Running my_wf() {my_wf()}")
