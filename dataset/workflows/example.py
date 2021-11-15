import pandas as pd

from flytekit import kwtypes, task, workflow
from flytekit.types.schema import SchemaFormat
from flytekit.types.structured.structured_dataset import FlyteDataset, FlyteDatasetMetadata

PARQUET_PATH = "/tmp/dataframe.pq"
BQ_PATH = "bq://photo-313016:flyte.new_table3"


@task(environment={"GOOGLE_APPLICATION_CREDENTIALS": "/opt/gcp.json"})
def t0() -> pd.DataFrame:
    return pd.DataFrame({"Name": ["Tom", "Joseph"], "Age": [20, 22]})

@task
def t1(dataframe: pd.DataFrame) -> FlyteDataset[FlyteDatasetMetadata(columns=kwtypes(x=int, y=str), path=PARQUET_PATH)]:
    # Pandas -> S3 (parquet)
    return dataframe


@task
def t2(dataframe: pd.DataFrame) -> pd.DataFrame:
    # Pandas -> Pandas
    return dataframe


@task
def t3(
    dataframe: FlyteDataset[FlyteDatasetMetadata(columns=kwtypes(x=int, y=str))]
) -> FlyteDataset[FlyteDatasetMetadata(columns=kwtypes(x=int, y=str))]:
    # s3 (parquet) -> pandas -> s3 (parquet)
    print(dataframe.open_as(pd.DataFrame))
    return dataframe


@task
def t4(dataframe: FlyteDataset[FlyteDatasetMetadata(columns=kwtypes(x=int, y=str))]) -> pd.DataFrame:
    # s3 (parquet) -> pandas -> s3 (parquet)
    return dataframe.open_as(pd.DataFrame)


@task
def t5(dataframe: pd.DataFrame) -> FlyteDataset[FlyteDatasetMetadata(columns=kwtypes(x=int, y=str), path=BQ_PATH)]:
    # pandas -> bq
    return dataframe


@task
def t6(
    dataframe: FlyteDataset[FlyteDatasetMetadata(columns=kwtypes(x=int, y=str), fmt=SchemaFormat.BIGQUERY)]
) -> pd.DataFrame:
    # pandas -> bq
    df = dataframe.open_as(pd.DataFrame)
    return df


@task(environment={"GOOGLE_APPLICATION_CREDENTIALS": "/opt/gcp.json"})
def t7(
    df1: pd.DataFrame, df2: pd.DataFrame
) -> (
    FlyteDataset[FlyteDatasetMetadata(columns=kwtypes(x=int, y=str), path=BQ_PATH)],
    FlyteDataset[FlyteDatasetMetadata(columns=kwtypes(x=int, y=str))],
):
    # df1: pandas -> bq
    # df2: pandas -> s3 (parquet)
    return df1, df2


@workflow()
def wf():
    df = t0()
    t7(df1=df, df2=df)


if __name__ == "__main__":
    wf()
