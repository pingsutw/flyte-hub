import datetime
import random
from operator import add

import flytekit
from flytekit import Resources, task, workflow
from flytekit.image_spec.image_spec import ImageSpec
from flytekitplugins.spark import Spark

spark_image = ImageSpec(base_image="pingsutw/spark-v2", registry="pingsutw")


@task(
    task_config=Spark(
        # this configuration is applied to the spark cluster
        spark_conf={
            "spark.driver.memory": "1000M",
            "spark.executor.memory": "1000M",
            "spark.executor.cores": "1",
            "spark.executor.instances": "2",
            "spark.driver.cores": "1",
        },
        executor_path="/usr/bin/python3",
        applications_path="local:///usr/local/bin/entrypoint.py",
    ),
    limits=Resources(mem="2000M"),
    cache_version="1",
    container_image=spark_image,
)
def hello_spark(partitions: int) -> float:
    print("Starting Sparkfk wifth Partitions: {}".format(partitions))
    n = 100000 * partitions
    sess = flytekit.current_context().spark_session
    count = (
        sess.sparkContext.parallelize(range(1, n + 1), partitions).map(f).reduce(add)
    )
    pi_val = 4.0 * count / n
    print("Pi val is :{}".format(pi_val))
    return pi_val


def f(_):
    x = random.random() * 2 - 1
    y = random.random() * 2 - 1
    return 1 if x**2 + y**2 <= 1 else 0


@task(cache_version="1", container_image=spark_image)
def print_every_time(value_to_print: float, date_triggered: datetime.datetime) -> int:
    print("My printed value: {} @ {}".format(value_to_print, date_triggered))
    return 1


@workflow
def wf(triggered_date: datetime.datetime = datetime.datetime.now()) -> float:
    """
    Using the workflow is still as any other workflow. As image is a property of the task, the workflow does not care
    about how the image is configured.
    """
    pi = hello_spark(partitions=50)
    print_every_time(value_to_print=pi, date_triggered=triggered_date)
    return pi


if __name__ == "__main__":
    print(f"Running {__file__} main...")
    print(
        f"Running my_spark(triggered_date=datetime.datetime.now()){wf(triggered_date=datetime.datetime.now())}"
    )
