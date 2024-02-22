import pandas as pd
from flytekit import ImageSpec, StructuredDataset, kwtypes, task, workflow
from flytekitplugins.bigquery import BigQueryConfig, BigQueryTask
from typing_extensions import Annotated

MyDataset = Annotated[StructuredDataset, kwtypes(name=str)]

image_spec = ImageSpec(
    name="flyte-hub",
    packages=[
        "flytekitplugins-bigquery",
        "google-cloud-bigquery-storage",
        "google-cloud-bigquery",
    ],
    registry="pingsutw",
)


@task(container_image=image_spec)
def create_bq_table() -> StructuredDataset:
    df = pd.DataFrame(data={"name": ["Alice", "bob"], "age": [5, 6]})
    return StructuredDataset(
        dataframe=df, uri="bq://dogfood-gcp-dataplane:dataset.flyte_table3"
    )


bigquery_task_templatized_query = BigQueryTask(
    name="bigquery",
    inputs=kwtypes(version=int),
    output_structured_dataset_type=MyDataset,
    task_config=BigQueryConfig(ProjectID="dogfood-gcp-dataplane"),
    query_template="SELECT * from dataset.flyte_table3;",  # type: ignore
)


@workflow
def bigquery_wf(version: int = 10) -> MyDataset:
    query = bigquery_task_templatized_query(version=version)
    create_bq_table() >> query
    return query
