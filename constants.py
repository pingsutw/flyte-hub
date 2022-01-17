from enum import Enum


class FlyteCluster(Enum):
    remote = "submarine.io:30081"
    local = "localhost:30081"
