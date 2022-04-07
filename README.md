# Multiple Container Images in a Single Workflow

- Build the image for task `say_hello`
```shell
docker build -t pingsutw/task1 -f Dockerfile . 
```

- Build the image for task `say_hi`
```shell
docker build -t pingsutw/task2 -f Dockerfile1 . 
```

- Package this Workflow
```shell
pyflyte --pkgs flyte package  --force
```

- Register this workflow to the sandbox
```shell
flytectl register files --archive -p flytesnacks -d development --archive flyte-package.tgz --version v1
```
