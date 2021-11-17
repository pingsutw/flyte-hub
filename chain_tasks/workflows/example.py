from flytekit import task, workflow
from flytekit.core.node_creation import create_node
import pandas as pd

DATABASE = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv"


@task
def read() -> pd.DataFrame:
    data = pd.read_csv(DATABASE)
    return data


@task
def write():
    # dummy code
    df = pd.DataFrame(
        data={
            "sepal_length": [5.3],
            "sepal_width": [3.8],
            "petal_length": [0.1],
            "petal_width": [0.3],
            "species": ["setosa"],
        }
    )


@workflow
def chain_tasks_wf() -> pd.DataFrame:
    write_node = create_node(write)
    read_node = create_node(read)

    write_node >> read_node

    return read_node.o0


if __name__ == "__main__":
    print(f"Running {__file__} main...")
    print(f"Running chain_tasks_wf()... {chain_tasks_wf()}")
