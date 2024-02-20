import os
import pathlib
import typing

from flytekit import ImageSpec, Resources, kwtypes, workflow
from flytekitplugins.papermill import NotebookTask

image_spec = ImageSpec(
    registry="pingsutw",
    packages=["flytekitplugins-papermill", "tensorflow==2.12.0"],
    apt_packages=["git"],
)

nb = NotebookTask(
    name="simple-nb",
    notebook_path=os.path.join(
        pathlib.Path(__file__).parent.absolute(), "nb_simple.ipynb"
    ),
    render_deck=True,
    requests=Resources(cpu="1", mem="2Gi"),
    limits=Resources(cpu="1", mem="2Gi"),
    container_image=image_spec,
    inputs=kwtypes(epochs=int),
    enable_deck=True,
)


@workflow
def nb_to_python_wf(f: int = 5):
    nb(epochs=f)


if __name__ == "__main__":
    print(nb_to_python_wf(f=3.14))
