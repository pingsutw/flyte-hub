import datetime
import os
import random
from operator import add

import flytekit
from flytekit import Resources, Secret, task, workflow
from flytekitplugins.spark import Databricks

SECRET_GROUP = "token-info"
SECRET_NAME = "token_secret"


@task(
    secret_requests=[
        Secret(
            group=SECRET_GROUP,
            key=SECRET_NAME,
            mount_requirement=Secret.MountType.ENV_VAR,
        )
    ],
    task_config=Databricks(
        # this configuration is applied to the spark cluster
        spark_conf={
            "spark.driver.memory": "1000M",
            "spark.executor.memory": "1000M",
            "spark.executor.cores": "1",
            "spark.executor.instances": "1",
            "spark.driver.cores": "1",
        },
        applications_path="dbfs:///FileStore/tables/entrypoint.py",
        databricks_conf={
            "run_name": "flytekit databricks plugin example",
            "new_cluster": {
                "spark_version": "11.0.x-scala2.12",
                "node_type_id": "r3.xlarge",
                "num_workers": 1,
                "aws_attributes": {
                    "availability": "ON_DEMAND",
                    "instance_profile_arn": "arn:aws:iam::590375264460:instance-profile/databricks-s3-role",
                },
            },
            "timeout_seconds": 3600,
            "max_retries": 1,
        },
        databricks_instance=os.environ["DATABRICKS_HOST"],
    ),
    limits=Resources(mem="2000M"),
)
def hello_spark(partitions: int) -> float:
    print("Starting Spark with Partitions: {}".format(partitions))

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


@task(cache_version="1")
def print_every_time(value_to_print: float, date_triggered: datetime.datetime) -> int:
    print("My printed value: {} @ {}".format(value_to_print, date_triggered))
    return 1


@workflow
def wf(
    triggered_date: datetime.datetime = datetime.datetime.now(),
) -> float:
    """
    Using the workflow is still as any other workflow. As image is a property of the task, the workflow does not care
    about how the image is configured.
    """
    pi = hello_spark(partitions=50)
    print_every_time(value_to_print=pi, date_triggered=triggered_date)
    return pi
