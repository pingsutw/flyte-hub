ARG BASE_IMAGE_VERSION
FROM pingsutw/base-${BASE_IMAGE_VERSION:-python3.7}-flyte-app

# RUN pip install markdown plotly pandas_profiling sklearn ray[]==1.13.0
WORKDIR /root
ARG BRANCH=master
ARG PLUGIN=ray
ARG IDL_BRANCH=master

RUN apt-get update && apt-get install -y git

# Install custom package
# RUN pip install mlflow plotly tensorflow
RUN pip install "git+https://github.com/flyteorg/flytekit@$BRANCH#egg=flytekitplugins-$PLUGIN&subdirectory=plugins/flytekit-$PLUGIN"
# RUN pip install git+https://github.com/flyteorg/flytekit@28ffc6346fd87c19f15d922e654280146ab3a40c
RUN pip install "git+https://github.com/flyteorg/flytekit@$BRANCH"
RUN pip install "git+https://github.com/flyteorg/flyteidl@$IDL_BRANCH"
RUN pip install awscli
RUN pip install -U ray[default] modin[ray] scikit-learn xgboost_ray tabulate

# Copy the actual code
COPY ./ /root
ENV PYTHONPATH /root
ENV PATH="/root:$PATH"
ENV FLYTE_SDK_LOGGING_LEVEL 10