"""
BigQuery Query
############

This example shows how to use a Flyte BigQueryTask to execute a query.
"""
import pandas as pd
from flytekit import StructuredDataset, kwtypes, task, workflow
from flytekitplugins.bigquery import BigQueryConfig, BigQueryTask
from typing_extensions import Annotated

# %%
# This is the world's simplest query. Note that in order for registration to work properly, you'll need to give your
# BigQuery task a name that's unique across your project/domain for your Flyte installation.
bigquery_task_no_io = BigQueryTask(
    name="sql.bigquery.no_io",
    inputs={},
    query_template="SELECT 1",
    output_schema_type=None,
    task_config=BigQueryConfig(ProjectID="flyte-test-340607"),
)


@workflow
def no_io_wf():
    return bigquery_task_no_io()


# %%
# Of course, in real world applications we are usually more interested in using BigQuery to query a dataset.
# In this case we use crypto_dogecoin data which is public dataset in BigQuery.
# `here <https://console.cloud.google.com/bigquery?project=bigquery-public-data&page=table&d=crypto_dogecoin&p=bigquery-public-data&t=transactions>`__
# The data is formatted according to this schema:
#
# Let's look out how we can parameterize our query to filter results for a specific transaction version, provided as a user input
# specifying a version.

DogeCoinDataset = Annotated[
    StructuredDataset, kwtypes(hash=str, size=int, block_number=int)
]

bigquery_task_templatized_query = BigQueryTask(
    name="sql.bigquery.w_io",
    # Define inputs as well as their types that can be used to customize the query.
    inputs=kwtypes(version=int),
    output_structured_dataset_type=StructuredDataset,
    task_config=BigQueryConfig(ProjectID="flyte-test-340607"),
    query_template="SELECT 1;",
)


@task
def convert_bq_table_to_pandas_dataframe(sd: StructuredDataset) -> pd.DataFrame:
    return sd.open(pd.DataFrame).all()


@workflow
def full_bigquery_wf(version: int = 1) -> pd.DataFrame:
    sd = bigquery_task_templatized_query(version=version)
    return convert_bq_table_to_pandas_dataframe(sd=sd)


# %%
# Check query result on bigquery console: ``https://console.cloud.google.com/bigquery``
