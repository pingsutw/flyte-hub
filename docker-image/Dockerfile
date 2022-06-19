# FROM pingsutw/base-spark-flyte-app
# base image version: [python3.7, python3.8, python3.9, python3.10, spark]
ARG BASE_IMAGE_VERSION
FROM pingsutw/base-${BASE_IMAGE_VERSION:-spark}-flyte-app

ENV FLYTE_SDK_USE_STRUCTURED_DATASET=True

RUN pip install markdown plotly pandas_profiling sklearn

ARG BRANCH=benchmark
ARG PLUGIN=deck-standard
ARG IDL_BRANCH=master

# Install custom package
RUN pip install "git+https://github.com/flyteorg/flytekit@$BRANCH#egg=flytekitplugins-$PLUGIN&subdirectory=plugins/flytekit-$PLUGIN"
RUN pip install git+https://github.com/flyteorg/flyteidl@$IDL_BRANCH
RUN pip install git+https://github.com/flyteorg/flytekit@$BRANCH

# Copy the actual code
COPY ./ /root

ENV FLYTE_SDK_LOGGING_LEVEL=20
