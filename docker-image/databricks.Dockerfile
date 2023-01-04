FROM databricksruntime/standard:11.3-LTS

ARG BRANCH=databricks-update
ARG PLUGIN=spark
ARG IDL_BRANCH=master

RUN sudo apt-get update && sudo apt-get install -y git

# Install custom package
RUN /databricks/python3/bin/pip install markupsafe==2.0.1 awscli
ARG TIME=bar
RUN /databricks/python3/bin/pip install "git+https://github.com/flyteorg/flytekit@$BRANCH#egg=flytekitplugins-$PLUGIN&subdirectory=plugins/flytekit-$PLUGIN"
# RUN pip install git+https://github.com/flyteorg/flytekit@28ffc6346fd87c19f15d922e654280146ab3a40c
RUN /databricks/python3/bin/pip install "git+https://github.com/flyteorg/flytekit@$BRANCH"
RUN /databricks/python3/bin/pip install "git+https://github.com/flyteorg/flyteidl@$IDL_BRANCH"

# RUN pip install flytekit==v1.2.0b1
# Copy the actual code
COPY ./ /databricks/driver
ENV PYTHONPATH /databricks/driver
ENV PATH="/databricks/python3/bin:$PATH"
ENV FLYTE_SDK_LOGGING_LEVEL 20
