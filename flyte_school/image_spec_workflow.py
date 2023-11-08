from flytekit import ImageSpec, task, workflow

image = ImageSpec(registry="pingsutw", packages=["tensorflow", "mypy", "numpy"])


@task(container_image=image)
def t1() -> None:
    import tensorflow

    print("hello")


@workflow
def wf():
    t1()
