import random

from flytekit import conditional, task, workflow


@task
def square(n: float) -> float:
    """
    Parameters:
        n (float): name of the parameter for the task will be derived from the name of the input variable
               the type will be automatically deduced to be Types.Integer
    Return:
        float: The label for the output will be automatically assigned and type will be deduced from the annotation
    """
    return n * n


@task
def double(n: float) -> float:
    """
    Parameters:
        n (float): name of the parameter for the task will be derived from the name of the input variable
               the type will be automatically deduced to be Types.Integer
    Return:
        float: The label for the output will be automatically assigned and type will be deduced from the annotation
    """
    return 2 * n


@workflow
def multiplier(my_input: float) -> float:
    return (
        conditional("fractions")
        .if_((my_input >= 0.1) & (my_input <= 1.0))
        .then(double(n=my_input))
        .else_()
        .then(square(n=my_input))
    )


if __name__ == "__main__":
    print(f"Output of multiplier(my_input=3.0): {multiplier(my_input=3.0)}")
    print(f"Output of multiplier(my_input=0.5): {multiplier(my_input=0.5)}")
