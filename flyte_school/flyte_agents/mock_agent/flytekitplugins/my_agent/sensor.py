import requests
from flytekit.sensor.base_sensor import BaseSensor


class FlyteReleaseSensor(BaseSensor):
    def __init__(self, name: str, **kwargs):
        super().__init__(name=name, **kwargs)

    async def poke(self, version: str) -> bool:
        print(f"Checking if {version} is released")

        url = f"https://github.com/flyteorg/flyte/tree/v{version}"
        response = requests.get(url)
        if response.status_code == 200:
            return True
        elif response.status_code == 404:
            return False
        print(f"Failed to check release existence. Status code: {response.status_code}")
        return False
