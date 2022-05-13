from typing_extensions import Annotated

import pandas as pd
import pyarrow as pa
from flytekit import FlyteContextManager, kwtypes, task, workflow
from flytekit.types.structured.structured_dataset import PARQUET, StructuredDataset

my_cols = kwtypes(Name=str, Age=int)
fields = [("Name", pa.string()), ("Age", pa.int32())]
arrow_schema = pa.schema(fields)
pd_df = pd.DataFrame({"Name": ["Tom", "Joseph"], "Age": [20, 22]})


@task
def t1(dataframe: pd.DataFrame) -> Annotated[pd.DataFrame, my_cols, PARQUET]:
    return dataframe


@task
def t2(dataframe: pd.DataFrame) -> Annotated[StructuredDataset, my_cols, PARQUET]:
    return StructuredDataset(dataframe=dataframe)


@task
def t3(dataframe: pd.DataFrame) -> Annotated[pd.DataFrame, arrow_schema]:
    return dataframe


@task
def t4(dataset: Annotated[StructuredDataset, my_cols, PARQUET]) -> pd.DataFrame:
    return dataset.open(pd.DataFrame).all()


@task
def t5(dataset: Annotated[StructuredDataset, my_cols, PARQUET]) -> pd.DataFrame:
    df = dataset.open(pd.DataFrame).all()
    return df


@task
def t6(dataframe: pa.Table) -> Annotated[StructuredDataset, my_cols, PARQUET]:
    print(dataframe.columns)
    return StructuredDataset(dataframe=dataframe)


@task
def t7(dataframe: pa.Table) -> pa.Table:
    print(dataframe.columns)
    return dataframe


@task
def generate_pandas() -> pd.DataFrame:
    return pd_df


@task
def generate_arrow() -> pa.Table:
    return pa.Table.from_pandas(
        pd.DataFrame({"Name": ["Tom", "Joseph"], "Age": [20, 22]})
    )


@workflow()
def wf():
    df = generate_pandas()
    arrow_df = generate_arrow()
    t1(dataframe=df)
    res = t2(dataframe=df)
    t3(dataframe=df)
    t5(dataset=res)
    t6(dataframe=arrow_df)
    t7(dataframe=arrow_df)


if __name__ == "__main__":
    wf()
