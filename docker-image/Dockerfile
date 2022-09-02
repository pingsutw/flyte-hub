# FROM pingsutw/base-spark-flyte-app
# base image version: [python3.7, python3.8, python3.9, python3.10, spark]
ARG BASE_IMAGE_VERSION
FROM pingsutw/base-${BASE_IMAGE_VERSION:-python3.7}-flyte-app

# RUN pip install markdown plotly pandas_profiling sklearn ray[]==1.13.0

ARG BRANCH=union-pickle
ARG PLUGIN=bigquery
ARG IDL_BRANCH=ray

# Install custom package
# RUN pip install "git+https://github.com/flyteorg/flytekit@$BRANCH#egg=flytekitplugins-$PLUGIN&subdirectory=plugins/flytekit-$PLUGIN"
# RUN pip install git+https://github.com/flyteorg/flytekit@$BRANCH
RUN pip install flytekit==v1.2.0b0
# Copy the actual code
COPY ./ /root
