FROM pingsutw/base-flyte-app

# Install custom package
# RUN git clone https://github.com/flyteorg/flytekit.git && cd flytekit && git checkout union_type && pip install . && cd ..
RUN git clone https://github.com/pingsutw/flytekit.git && cd flytekit && git checkout schema-arrow-ping && pip install . && cd ..
RUN git clone https://github.com/flyteorg/flyteidl.git && cd flyteidl && git checkout new-schema && pip install . && cd ..
