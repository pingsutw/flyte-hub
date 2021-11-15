from flytekit import task, workflow
import typing


class Dog:
    def __init__(self, name):
        self.name = name


@task
def greet(name: str) -> typing.List[Dog]:
    dog = Dog(name)
    return [dog]


@task
def add_question(greeting: typing.List[Dog]) -> str:
    return f"{greeting[0].name} How are you?"


@workflow
def welcome(name: str) -> str:
    greeting = greet(name=name)
    return add_question(greeting=greeting)


if __name__ == "__main__":
    print(welcome(name="Kevin"))

