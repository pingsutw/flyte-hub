# FROM pingsutw/base-spark-flyte-app
# base image version: [python3.7, python3.8, python3.9, python3.10, spark]
ARG BASE_IMAGE_VERSION
FROM pingsutw/base-${BASE_IMAGE_VERSION:-python3.9}-flyte-app

# Copy the actual code
COPY ./ /root

# Install custom package
# RUN git clone https://github.com/flyteorg/flytekit.git && cd flytekit && git checkout bigquery && pip install . && \
 # cd plugins/flytekit-bigquery && pip install --no-deps -e . && cd .. \
# RUN git clone https://github.com/flyteorg/flytekit.git && cd flytekit && git checkout union_type && pip install . && cd ..
# RUN git clone https://github.com/flyteorg/flytekit.git && cd flytekit && git checkout deprecate_arrayjob_proto && pip install . && cd ..
RUN git clone https://github.com/flyteorg/flytekit.git && cd flytekit && git checkout master && pip install . && cd ..

