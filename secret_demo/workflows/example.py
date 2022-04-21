import os
import flytekit
from typing import Tuple

from flytekit import Secret, task, workflow
from flytekit.testing import SecretsManager


SECRET_NAME = "user_secret"
SECRET_GROUP = "user-info"

USERNAME_SECRET = "username"
PASSWORD_SECRET = "password"


@task(secret_requests=[Secret(group=SECRET_GROUP, key=SECRET_NAME)], disable_deck=True)
def secret_task() -> str:
    secret_val = flytekit.current_context().secrets.get(SECRET_GROUP, SECRET_NAME)
    # Please do not print the secret value, we are doing so just as a demonstration
    print(secret_val)
    return secret_val


@task(
    secret_requests=[Secret(key=USERNAME_SECRET, group=SECRET_GROUP), Secret(key=PASSWORD_SECRET, group=SECRET_GROUP)],
    disable_deck=True)
def user_info_task() -> Tuple[str, str]:
    secret_username = flytekit.current_context().secrets.get(SECRET_GROUP, USERNAME_SECRET)
    secret_pwd = flytekit.current_context().secrets.get(SECRET_GROUP, PASSWORD_SECRET)
    # Please do not print the secret value, this is just a demonstration.
    print(f"{secret_username}={secret_pwd}")
    return secret_username, secret_pwd


@task(secret_requests=[Secret(group=SECRET_GROUP, key=SECRET_NAME, mount_requirement=Secret.MountType.ENV_VAR)],
      disable_deck=True)
def secret_file_task() -> Tuple[str, str]:
    # SM here is a handle to the secrets manager
    sm = flytekit.current_context().secrets
    f = sm.get_secrets_file(SECRET_GROUP, SECRET_NAME)
    secret_val = sm.get(SECRET_GROUP, SECRET_NAME)
    # returning the filename and the secret_val
    return f, secret_val


@workflow
def my_secret_workflow() -> Tuple[str, str, str, str, str]:
    x = secret_task()
    y, z = user_info_task()
    f, s = secret_file_task()
    return x, y, z, f, s


if __name__ == "__main__":
    sec = SecretsManager()
    os.environ[sec.get_secrets_env_var(SECRET_GROUP, SECRET_NAME)] = "value"
    os.environ[sec.get_secrets_env_var(SECRET_GROUP, USERNAME_SECRET)] = "username_value"
    os.environ[sec.get_secrets_env_var(SECRET_GROUP, PASSWORD_SECRET)] = "password_value"
    x, y, z, f, s = my_secret_workflow()
    assert x == "value"
    assert y == "username_value"
    assert z == "password_value"
    assert f == sec.get_secrets_file(SECRET_GROUP, SECRET_NAME)
    assert s == "value"
