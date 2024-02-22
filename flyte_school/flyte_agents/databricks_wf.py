import datetime
import random
from operator import add

import flytekit
from flytekit import ImageSpec, Resources, task, workflow
from flytekitplugins.spark import Databricks

image = ImageSpec(base_image="flyteorg/flytekit:spark-latest", registry="pingsutw")


@task(
    task_config=Databricks(
        # this configuration is applied to the spark cluster
        spark_conf={
            "spark.driver.memory": "600M",
            "spark.executor.memory": "600M",
            "spark.executor.cores": "1",
            "spark.executor.instances": "1",
            "spark.driver.cores": "1",
        },
        executor_path="/databricks/python3/bin/python",
        applications_path="dbfs:///FileStore/tables/entrypoint.py",
        databricks_conf={
            "run_name": "flytekit databricks plugin example",
            "job_id": "{{inputs.cluster_id}}",
            "new_cluster": {
                "spark_version": "13.3.x-scala2.12",
                "node_type_id": "m6i.large",  # TODO: test m6i.large, i3.xlarge
                "num_workers": 3,
                "aws_attributes": {
                    "availability": "SPOT_WITH_FALLBACK",
                    "instance_profile_arn": "arn:aws:iam::546011168256:instance-profile/databricks-demo",
                    "ebs_volume_type": "GENERAL_PURPOSE_SSD",
                    "ebs_volume_count": 1,
                    "ebs_volume_size": 100,
                    "first_on_demand": 1,
                },
                "policy_id": "0000FF579DC57A49",
            },
            # "existing_cluster_id": "1122-085119-brus1mft",
            "timeout_seconds": 3600,
            "max_retries": 1,
        },
        databricks_instance="dbc-429786b4-2d97.cloud.databricks.com",
    ),
    limits=Resources(mem="2000M"),
    # container_image=imageee,
    container_image="pingsutw/databricks:v12",
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
    pi = hello_spark(partitions=50).with_overrides(name="my cluster")
    print_every_time(value_to_print=pi, date_triggered=triggered_date)
    return pi
