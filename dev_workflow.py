# Work in progress
# import conditional.workflows.example
# remote.execute(conditional.workflows.example.multiplier, inputs={"my_input", 3.0}, wait=False)
# import union_type.workflows.example
# remote.execute(union_type.workflows.example.wf, inputs={"a": 3}, version=version, wait=False)
# import bigquery.workflows.example
# remote.execute(bigquery.workflows.example.full_bigquery_wf, inputs={"version": 1}, version=version, wait=False)
# import spark_dataframe.workflows.example
# remote.execute(spark_dataframe.workflows.example.my_smart_schema, inputs={}, version=version, wait=False)
# import dynamic.workflows.example
# remote.execute(dynamic.workflows.example.wf, inputs={"s1": "1", "s2": "2"}, version=version, wait=False)
# import enum_types.workflows.example
# remote.execute(enum_types.workflows.example.enum_wf, inputs={"c": "RED"}, wait=False)
# import raw_container.workflows.example
# remote.execute(raw_container.workflows.example.wf, inputs={"a": 2.0, "b": 3.0}, wait=False)
import test.workflows.example

from utils import register_and_create_wf

register_and_create_wf(test.workflows.example.wf)
