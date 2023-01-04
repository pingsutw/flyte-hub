ARG PYTHON_VERSION
FROM python:${PYTHON_VERSION:-3.9}-slim

WORKDIR /root

# Install custom package
RUN pip install flytekitplugins-awsbatch
RUN pip install awscli

# Copy the actual code
COPY ./ /root
ENV PYTHONPATH /root
ENV FLYTE_SDK_LOGGING_LEVEL 20