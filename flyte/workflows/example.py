from flytekit import task, workflow

# The tasks below are using different docker image
# We may want to use a better example than this


@task(container_image="pingsutw/task1")
def say_hello() -> str:
    return "hello world"


@task(container_image="pingsutw/task2")
def say_hi() -> str:
    return "Hi"


@workflow
def my_wf() -> str:
    res = say_hello()
    return res


if __name__ == "__main__":
    print(f"Running my_wf() { my_wf() }")
