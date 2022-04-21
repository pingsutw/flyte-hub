# FROM pingsutw/base-spark-flyte-app
# base image version: [python3.7, python3.8, python3.9, python3.10, spark]
ARG BASE_IMAGE_VERSION
FROM pingsutw/base-${BASE_IMAGE_VERSION:-spark}-flyte-app

# Copy the actual code
COPY ./ /root

ENV FLYTE_SDK_USE_STRUCTURED_DATASET=True

RUN pip install markdown plotly pandas_profiling

ARG BRANCH=remote-deck
ARG PLUGIN=flytekit-deck-standard

# Install custom package
RUN git clone https://github.com/flyteorg/flytekit.git && cd flytekit \
    && git checkout $BRANCH && pip install . && \
   cd plugins/$PLUGIN && pip install --no-deps -e . && cd ..

