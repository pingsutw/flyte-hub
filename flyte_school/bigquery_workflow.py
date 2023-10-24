from typing_extensions import Annotated

import pandas as pd
from flytekit import StructuredDataset, kwtypes, task, workflow
from flytekitplugins.bigquery import BigQueryConfig, BigQueryTask


DogeCoinDataset = Annotated[StructuredDataset, kwtypes(hash=str, size=int, block_number=int)]

bigquery_task_templatized_query = BigQueryTask(
    name="sql.bigquery.w_io",
    # Define inputs as well as their types that can be used to customize the query.
    inputs=kwtypes(version=int),
    output_structured_dataset_type=DogeCoinDataset,
    task_config=BigQueryConfig(ProjectID="flyte"),
    query_template="SELECT * FROM `bigquery-public-data.crypto_dogecoin.transactions` WHERE version = @version LIMIT 10;",
)


@task
def convert_bq_table_to_pandas_dataframe(sd: DogeCoinDataset) -> pd.DataFrame:
    return sd.open(pd.DataFrame).all()


@workflow
def full_bigquery_wf(version: int) -> pd.DataFrame:
    sd = bigquery_task_templatized_query(version=version)
    return convert_bq_table_to_pandas_dataframe(sd=sd)
