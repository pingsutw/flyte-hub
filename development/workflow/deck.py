import flytekit
import pandas as pd
import plotly.express as px
from flytekit import task, workflow
from flytekit.deck.renderer import TopFrameRenderer
from flytekitplugins.deck.renderer import BoxRenderer, MarkdownRenderer
from typing_extensions import Annotated

iris_df = px.data.iris()


@task()
def t1(a: int) -> str:
    md_text = "#Hello Flyte\n##Hello Flyte\n###Hello Flyte"
    flytekit.Deck("demo", BoxRenderer("sepal_length").to_html(iris_df))
    flytekit.current_context().default_deck.append(MarkdownRenderer().to_html(md_text))
    return md_text


@task()
def t2(a: int) -> Annotated[pd.DataFrame, TopFrameRenderer(10)]:
    return iris_df


@task()
def t3(a: int):
    print("hello")


@workflow
def wf():
    t1(a=3)
    t2(a=2)
    t3(a=1)


if __name__ == "__main__":
    wf()
