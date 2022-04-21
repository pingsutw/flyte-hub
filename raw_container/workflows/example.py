import logging
from flytekit import task, workflow
from flytekit import ContainerTask, kwtypes, workflow

logger = logging.getLogger(__file__)

calculate_ellipse_area_shell = ContainerTask(
    name="ellipse-area-metadata-shell",
    input_data_dir="/var/inputs",
    output_data_dir="/var/outputs",
    inputs=kwtypes(a=float, b=float),
    outputs=kwtypes(area=float, metadata=str),
    image="pingsutw/raw:v7",
    command=[
        "/bin/bash",
        "-c",
        "./calculate-ellipse-area.sh /var/inputs /var/outputs;",
    ],
)


@task
def report_all_calculated_areas(
    area_shell: float,
    metadata_shell: str,
):
    logger.info(f"shell: area={area_shell}, metadata={metadata_shell}")


@workflow
def wf(a: float, b: float):
    area_shell, metadata_shell = calculate_ellipse_area_shell(a=a, b=b)
    report_all_calculated_areas(
        area_shell=area_shell,
        metadata_shell=metadata_shell,
    )


if __name__ == "__main__":
    print(f"Running wf() {wf(a=2.0, b=3.0)}")
