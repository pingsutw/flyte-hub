from flytekit import task, workflow
from flytekitplugins.bigquery import BigQueryConfig, BigQueryTask

bigquery_task = BigQueryTask(
    name="flytekit.demo.bigquery_task.query",
    task_config=BigQueryConfig(ProjectID="Flyte", Location="Asia"),
    query_template="select 1",
)


@task
def t1():
    print("t1")


@task
def t2():
    print("t2")


@task
def t3():
    print("t3")


@workflow
def wf():
    print("flyte")
    BigQueryTask()
    t1() >> t2() >> t3()


if __name__ == "__main__":
    wf()
