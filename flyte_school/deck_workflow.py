import pandas as pd

import flytekit
from flytekit import task, workflow, ImageSpec
from flytekitplugins.deck.renderer import FrameProfilingRenderer

image_spec = ImageSpec(registry="pingsutw", packages=["flytekitplugins-deck-standard"])


@task(enable_deck=True, container_image=image_spec)
def frame_renderer() -> None:
    df = pd.DataFrame(data={"col1": [1, 2], "col2": [3, 4]})
    flytekit.Deck("Frame Renderer", FrameProfilingRenderer().to_html(df=df))


@workflow
def wf():
    frame_renderer()
