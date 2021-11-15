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
  a: APP_NAME or the REPOSITORY APP_NAME. Defaults to myapp.
  r = REGISTRY name where the docker container should be pushed. Defaults to none - localhost
  v = VERSION of the build. Defaults to using the current git head SHA
```
- For example:
```bash
./start_example.sh -a myapp -v v1
```
- Output will be like
```bash
myapp-v2: digest: sha256:03c59ea7591d9e43e8ceba795dd76ea5af8fe561702c4fd2d78200c08f0e862c size: 3264
Configuration file 'flytekit.config' could not be loaded. Using values from environment.
Flyte Admin URL None
Loading packages ('myapp',) under source root /Users/kevin/git/flyte-app
hello
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

## NOTE
1. Once you have acquainted yourself, update the root package name from ``myapp`` -> ``your actual appnamee``
2. This APP name is also added to ``docker_build_and_tag.sh`` - ``APP_NAME``
3. We recommend using a git repository and this the ``docker_build_and_tag.sh``
   to build your docker images
4. We also recommend using pip-compile to build your requirements.
