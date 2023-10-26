from flytekit import task, workflow, ImageSpec


image_spec = ImageSpec(registry="pingsutw", packages=["tensorflow", "mypy"])


@task(container_image=image_spec)
def t1() -> None:
    import tensorflow
    print("hello")


@workflow
def wf():
    t1()
