from flytekit import Resources, task, workflow
from flytekitplugins.ray import HeadNodeConfig, RayJobConfig, WorkerNodeConfig
from ray import tune
from sklearn.datasets import load_breast_cancer
from xgboost_ray import RayDMatrix, RayParams, train

ray_config = RayJobConfig(
    head_node_config=HeadNodeConfig(ray_start_params={"log-color": "True"}),
    worker_node_config=[WorkerNodeConfig(group_name="ray-group", replicas=2)],
)

ray_params = RayParams(num_actors=4, cpus_per_actor=1)


def train_model(config):
    train_x, train_y = load_breast_cancer(return_X_y=True)
    train_set = RayDMatrix(train_x, train_y)

    evals_result = {}
    bst = train(
        params=config,
        dtrain=train_set,
        evals_result=evals_result,
        evals=[(train_set, "train")],
        verbose_eval=False,
        ray_params=ray_params,
    )
    bst.save_model("model.xgb")


@task(
    task_config=ray_config,
    requests=Resources(mem="1G", cpu="2", ephemeral_storage="1G"),
    limits=Resources(mem="2G", cpu="2", ephemeral_storage="1G"),
)
def train_model_task() -> dict:
    config = {
        "tree_method": "approx",
        "objective": "binary:logistic",
        "eval_metric": ["logloss", "error"],
        "eta": tune.loguniform(1e-4, 1e-1),
        "subsample": tune.uniform(0.5, 1.0),
        "max_depth": tune.randint(1, 9),
    }

    analysis = tune.run(
        train_model,
        config=config,
        metric="train-error",
        mode="min",
        num_samples=4,
        max_concurrent_trials=1,
        resources_per_trial=ray_params.get_tune_resources(),
    )
    return analysis.best_config


@workflow
def wf() -> dict:
    return train_model_task()


if __name__ == "__main__":
    print(wf())
