import io

import flytekit
import pandas as pd
import plotly.express as px
import requests
from flytekit import ImageSpec, task, workflow
from flytekit.deck.renderer import TopFrameRenderer
from flytekitplugins.deck.renderer import BoxRenderer, MarkdownRenderer
from typing_extensions import Annotated

iris_df = px.data.iris()
image_spec = ImageSpec(
    base_image="python:3.8-slim-buster", packages=["pillow"], registry="pingsutw"
)


@task(cache_version="2.0", cache=True)
def t1() -> str:
    md_text = "#Hello Flyte\n##Hello Flyte\n###Hello Flyte"
    flytekit.Deck("demo", BoxRenderer("sepal_length").to_html(iris_df))
    flytekit.current_context().default_deck.append(MarkdownRenderer().to_html(md_text))
    return md_text


@task(cache_version="2.0", cache=True)
def t2() -> Annotated[pd.DataFrame, TopFrameRenderer(10)]:
    return iris_df


@task(container_image=image_spec)
def t3():
    import PIL.Image

    url = "https://miro.medium.com/v2/resize:fit:1400/1*0T9PjBnJB9H0Y4qrllkJtQ.png"
    response = requests.get(url)
    image_bytes = io.BytesIO(response.content)
    im = PIL.Image.open(image_bytes)
    return im


@workflow
def wf():
    t1()
    t2()
    t3()


if __name__ == "__main__":
    wf()
