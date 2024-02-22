FROM python:3.9-slim-buster

MAINTAINER Flyte Team <users@flyte.org>
LABEL org.opencontainers.image.source=https://github.com/flyteorg/flytekit

RUN apt-get update && apt-get install -y git build-essential

RUN pip install prometheus_client
RUN pip install flytekitplugins-airflow
RUN pip install "git+https://github.com/flyteorg/flytekit.git@f6fae6787c00831878d119019eb5b76bb7b1f602#subdirectory=plugins/flytekit-spark"
RUN pip install "git+https://github.com/flyteorg/flytekit.git@f6fae6787c00831878d119019eb5b76bb7b1f602#subdirectory=plugins/flytekit-airflow"
RUN pip install "git+https://github.com/flyteorg/flytekit.git@f6fae6787c00831878d119019eb5b76bb7b1f602"
RUN pip install "git+https://github.com/flyteorg/flyte.git@672bc3ed9362b484a5037ea77c5c9898f7903267#subdirectory=flyteidl"


COPY ./ /root/mock_agent
RUN pip install /root/mock_agent
WORKDIR /root

CMD pyflyte serve agent --port 8000
