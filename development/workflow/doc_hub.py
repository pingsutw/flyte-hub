from flytekit import Description, Documentation, SourceCode, task, workflow


@task()
def t1(a: int):
    """
    This is a class for mathematical operations on complex numbers.

    I am a long_description! I am a long_description! I am a long_description! I am a long_description!.

    Attributes:
        a (int): The real part of complex number.
    """
    print("hello")
    print(a)


@workflow(
    docs=Documentation(
        short_description="hello world",
        long_description=Description(uri="/Users/kevin/example.py"),
    )
)
def wf(a: int = 3):
    t1(a=a)


if __name__ == "__main__":
    wf(a=3)
