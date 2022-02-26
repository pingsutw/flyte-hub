import typing

from flytekit import task, workflow


class Dog:
    def __init__(self, name):
        self.name = name


@task()
def greet(name: str) -> typing.List[Dog]:
    dog = Dog(name)
    return [dog]


@task()
def add_question(dogs: typing.List[Dog]) -> typing.List[Dog]:
    return dogs


@workflow
def welcome(name: str) -> typing.List[Dog]:
    dogs = greet(name=name)
    return add_question(dogs=dogs)


if __name__ == "__main__":
    print(welcome(name="Kevin"))
