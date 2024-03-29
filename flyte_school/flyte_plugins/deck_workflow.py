import io

import flytekit
import pandas as pd
import PIL.Image
import requests
from flytekit import ImageSpec, task, workflow
from flytekitplugins.deck.renderer import FrameProfilingRenderer, TableRenderer
from sklearn.datasets import load_diabetes

image_spec = ImageSpec(
    registry="pingsutw", packages=["flytekitplugins-deck-standard", "pillow"]
)


@task(enable_deck=True, container_image=image_spec)
def frame_renderer() -> None:
    diabetes = load_diabetes()
    df = pd.DataFrame(data=diabetes.data, columns=diabetes.feature_names)
    flytekit.Deck("Frame Renderer", FrameProfilingRenderer().to_html(df=df))


@task(enable_deck=True, container_image=image_spec)
def table_renderer() -> None:
    diabetes = load_diabetes()
    df = pd.DataFrame(data=diabetes.data, columns=diabetes.feature_names)
    flytekit.Deck(
        "Table Renderer",
        TableRenderer().to_html(df=df, table_width=50),
    )


class ImageRenderer:
    def __init__(self, img_format="PNG"):
        self._img_format = img_format

    def to_html(self, image: PIL.Image.Image) -> str:
        import base64
        from io import BytesIO

        buffered = BytesIO()
        image.save(buffered, format=self._img_format)
        img_base64 = base64.b64encode(buffered.getvalue()).decode()
        return f'<img src="data:image/png;base64,{img_base64}" alt="Rendered Image" />'


@task(enable_deck=True, container_image=image_spec)
def image_renderer() -> None:
    url = "https://insightpestnorthwest.com/wp-content/uploads/2021/04/andrea-leopardi-QfhbK2pY0Ao-unsplash-1-1024x683.jpg"
    response = requests.get(url)
    image_bytes = io.BytesIO(response.content)
    im = PIL.Image.open(image_bytes)
    flytekit.Deck(
        "PIL Image",
        ImageRenderer().to_html(im),
    )


@workflow
def wf():
    frame_renderer()
    table_renderer()
    image_renderer()


if __name__ == "__main__":
    wf()
