from flyteidl.core.execution_pb2 import TaskExecution
from flytekit.extend.backend.base_agent import AgentRegistry, Resource, SyncAgentBase
from flytekit.models.literals import LiteralMap
from flytekit.models.task import TaskTemplate


class MockOpenAIAgent(SyncAgentBase):
    name = "Mock OpenAI Agent"

    def __init__(self):
        super().__init__(task_type_name="mock_openai")

    def do(
        self, task_template: TaskTemplate, inputs: LiteralMap = None, **kwargs
    ) -> Resource:
        print("Calling OpenAI...")
        print(f"Prompt: {inputs.literals['prompt'].scalar.primitive.string_value}")
        output = {
            "o0": "Flyte is a scalable and flexible workflow orchestration platform."
        }
        return Resource(phase=TaskExecution.SUCCEEDED, outputs=output)


AgentRegistry.register(MockOpenAIAgent(), override=True)
