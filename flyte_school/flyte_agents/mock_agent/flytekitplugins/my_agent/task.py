from flytekit.core.base_task import PythonTask, kwtypes
from flytekit.core.interface import Interface
from flytekit.extend.backend.base_agent import SyncAgentExecutorMixin


class MockOpenAITask(SyncAgentExecutorMixin, PythonTask):
    def __init__(self, **kwargs):
        super().__init__(
            task_type="mock_openai",
            task_config={},
            interface=Interface(inputs=kwtypes(prompt=str), outputs=kwtypes(o0=str)),
            **kwargs,
        )
