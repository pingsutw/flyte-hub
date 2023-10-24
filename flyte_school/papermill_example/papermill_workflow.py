import math

from flytekit import ImageSpec, task
import os
import pathlib

from flytekit import kwtypes, workflow
from flytekitplugins.papermill import NotebookTask


image = ImageSpec(packages=["flytekitplugins-papermill"], registry="pingsutw")


nb = NotebookTask(
    name="simple-nb",
    notebook_path=os.path.join(pathlib.Path(__file__).parent.absolute(), "nb_simple.ipynb"),
    render_deck=True,
    container_image=image,
    inputs=kwtypes(v=float),
    outputs=kwtypes(square=float),
    enable_deck=True,
)


@task(container_image=image)
def square_root_task(f: float) -> float:
    return math.sqrt(f)


@workflow
def nb_to_python_wf(f: float = 2.0):
    out = nb(v=f)


if __name__ == "__main__":
    print(nb_to_python_wf(f=3.14))
