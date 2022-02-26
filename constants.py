from enum import Enum


class FlyteCluster(Enum):
    flyte = "flyte.io:30081"
    submarine = "submarine.io:30081"
    local = "localhost:30081"
    union = "dns:///demo.nuclyde.io"
