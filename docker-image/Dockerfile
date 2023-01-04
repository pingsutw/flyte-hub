ARG PYTHON_VERSION
FROM python:${PYTHON_VERSION:-3.9}-slim

WORKDIR /root
ARG BRANCH=doc-hub
ARG PLUGIN=mlflow
ARG IDL_BRANCH=master

RUN apt-get update && apt-get install -y git

# Install custom package
# RUN pip install "git+https://github.com/flyteorg/flytekit@$BRANCH#egg=flytekitplugins-$PLUGIN&subdirectory=plugins/flytekit-$PLUGIN"
RUN pip install "git+https://github.com/flyteorg/flytekit@$BRANCH"
RUN pip install "git+https://github.com/flyteorg/flyteidl@$IDL_BRANCH"
RUN pip install awscli

# Copy the actual code
COPY ./ /root
ENV PYTHONPATH /root
ENV FLYTE_SDK_LOGGING_LEVEL 20