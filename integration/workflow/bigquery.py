import pandas as pd
from flytekit import task, StructuredDataset
import os
os.environ["GOOGLE_CLOUD_PROJECT"] = "flyte-test-340607"


@task
def my_task() -> StructuredDataset:
    df = pd.DataFrame({"Name": ["Tom", "Joseph"], "Age": [20, 22]})
    return StructuredDataset(dataframe=df, uri='bq://flyte-test-340607.dataset.test1')


@task
def my_task1(sd: StructuredDataset) -> pd.DataFrame:
    return sd.open(pd.DataFrame).all()


res = my_task1(sd=StructuredDataset(uri="bq://sp-one-model.quarterly_forecast_2022F1.premium_revenue_tab_input_vat"))
print(res)
# print(sd.open(pd.DataFrame).all())
