from flytekit import workflow
from flytekitplugins.chatgpt import ChatGPTTask

chatgpt_new_job = ChatGPTTask(
    name="chatgpt",
    openai_organization="org-P2rdnZQry4Fw7Ak3vSpXEIrx",
    chatgpt_config={
        "model": "gpt-3.5-turbo",
        "temperature": 0.7,
    },
)


@workflow
def wf(message: str = "hi") -> str:
    return chatgpt_new_job(message=message)


if __name__ == "__main__":
    print(wf())
