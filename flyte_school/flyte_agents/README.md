# Deploy Agent to the Flyte Cluster

```bash
helm repo add flyteagent https://flyteorg.github.io/flyteagent
helm install flyteschool-agent flyteorg/flyteagent --namespace flyte --set nameOverride=flyteschool-agent --set image.repository=pingsutw/flyte-school --set image.tag=agent-amd64
```
