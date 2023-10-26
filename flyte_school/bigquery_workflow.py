from flytekitplugins.bigquery import BigQueryConfig, BigQueryTask
from typing_extensions import Annotated

import pandas as pd
from flytekit import StructuredDataset, kwtypes, task, workflow
import pyarrow as pa

MyDataset = Annotated[StructuredDataset, kwtypes(name=str, age=int)]

@task
def create_bq_table() -> StructuredDataset:
    df = pd.DataFrame(data={"name": ["Alice", "bob"], "age": [5, 6]})
    return StructuredDataset(dataframe=df, uri="bq://flyte-test-340607:dataset.flyte_table3")


bigquery_task_templatized_query = BigQueryTask(
    name="bigquery_task",
    inputs=kwtypes(version=int),
    output_structured_dataset_type=MyDataset,
    task_config=BigQueryConfig(ProjectID="flyte-test-340607"),
    query_template='SELECT * from dataset.flyte_table3;',  # type: ignore
)


@task
def convert_bq_table_to_pandas_dataframe(sd: MyDataset) -> pa.Table:
    t = sd.open(pa.Table).all()
    print(t)
    return t


@workflow
def wf(version: int = 10) -> pa.Table:
    create_bq_table()
    sd = bigquery_task_templatized_query(version=version)
    return convert_bq_table_to_pandas_dataframe(sd=sd)


if __name__ == '__main__':
    wf()
