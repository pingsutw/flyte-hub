# flyte-app

- Flyte example - contains many kind of flyte examples for new users
- Flyte benchmark - microbenchmark testing for evaluating Flyte performance

## Prerequisite
Install python dependencies
```bash
pip install -r requirements.txt
```

## Usage
```bash
Usage: ./start_example.sh [-h|[-a <app_name>][-r <registry_name>][-v <version>]]
  h: help (this message)
  a = APP_NAME or the REPOSITORY APP_NAME. Defaults to myapp.
  r = REGISTRY name where the docker container should be pushed. Defaults to none - localhost
  v = VERSION of the build. Defaults to using the current git head SHA
  b = BASE_IMAGE_VERSION of the build (python3.7~python3.10, spark). Defaults to using the python3.8.
```
## Quick Start (flytectl)
```bash
./start_example.sh -a myapp -v v1
```
- Output will be like
```bash
myapp-v1: digest: sha256:03c59ea7591d9e43e8ceba795dd76ea5af8fe561702c4fd2d78200c08f0e862c size: 3264
Configuration file 'flytekit.config' could not be loaded. Using values from environment.
Flyte Admin URL None
Loading packages ('myapp',) under source root /Users/kevin/git/flyte-app
  Packaging myapp.workflows.example.say_hello -> 0_myapp.workflows.example.say_hello_1.pb
  Packaging myapp.workflows.example.my_wf -> 1_myapp.workflows.example.my_wf_2.pb
  Packaging myapp.workflows.example.my_wf -> 2_myapp.workflows.example.my_wf_3.pb
Successfully packaged 3 flyte objects into /Users/kevin/git/flyte-app/flyte-package.tgz
{"json":{"src":"client.go:244"},"level":"warning","msg":"Starting an unauthenticated client because: failed to fetch auth metadata. Error: rpc error: code = Unimplemented desc = unknown service flyteidl.service.AuthMetadataService","ts":"2021-11-15T20:00:03+08:00"}
{"json":{"src":"client.go:57"},"level":"info","msg":"Initialized Admin client","ts":"2021-11-15T20:00:03+08:00"}
{"json":{"src":"files.go:111"},"level":"info","msg":"Parsing file... Total(3)","ts":"2021-11-15T20:00:03+08:00"}
 ----------------------------------------------------------------- --------- ------------------------------ 
| NAME                                                            | STATUS  | ADDITIONAL INFO              |
 ----------------------------------------------------------------- --------- ------------------------------ 
| /tmp/register228055126/0_myapp.workflows.example.say_hello_1.pb | Success | Successfully registered file |
 ----------------------------------------------------------------- --------- ------------------------------ 
| /tmp/register228055126/1_myapp.workflows.example.my_wf_2.pb     | Success | Successfully registered file |
 ----------------------------------------------------------------- --------- ------------------------------ 
| /tmp/register228055126/2_myapp.workflows.example.my_wf_3.pb     | Success | Successfully registered file |
 ----------------------------------------------------------------- --------- ------------------------------ 
```

## Quick Start II (flytekit)
```python
from utils import create_flyte_remote
from constants import FlyteCluster
import myapp.workflows.example

remote, version = create_flyte_remote(url=FlyteCluster.local)
remote.execute(myapp.workflows.example.my_wf, inputs={}, version=version, wait=False)
```
- Output will be like
```bash
id {
  project: "flyteexamples"
  domain: "development"
  name: "f5121a2abc9d44da9855"
}
spec {
  launch_plan {
    resource_type: LAUNCH_PLAN
    project: "flyteexamples"
    domain: "development"
    name: "myapp.workflows.example.my_wf"
    version: "79a2451f18dbb7267edf0a839ea4d281"
  }
...
```