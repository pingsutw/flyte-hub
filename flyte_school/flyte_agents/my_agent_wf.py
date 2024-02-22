from flytekit import task, workflow
from flytekitplugins.my_agent import MockOpenAITask

openai_task = MockOpenAITask(name="openai")


@workflow
def wf(question: str = "What is Flyte") -> str:
    return openai_task(prompt=question)


if __name__ == "__main__":
    print(wf())
