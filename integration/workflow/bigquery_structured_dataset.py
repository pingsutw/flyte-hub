import os

import pandas as pd
import pyarrow
from flytekit import StructuredDataset, task

os.environ["GOOGLE_CLOUD_PROJECT"] = "flyte-test-340607"


@task
def pandas_dataframe_to_bq_table() -> StructuredDataset:
    df = pd.DataFrame({"Name": ["Tom", "Joseph"], "Age": [20, 22]})
    return StructuredDataset(dataframe=df, uri="bq://flyte-test-340607.dataset.test1")


@task
def bq_table_to_dataframe(sd: StructuredDataset) -> pd.DataFrame:
    # convert to pandas dataframe
    return sd.open(pd.DataFrame).all()
    # we could also convert it to arrow table
    # return sd.open(pyarrow.table).all()


if __name__ == "__main__":
    bq_table_to_dataframe(
        sd=StructuredDataset(uri="bq://flyte-test-340607.dataset.test1")
    )
    pandas_dataframe_to_bq_table()
