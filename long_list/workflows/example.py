from typing import List

from flytekit import task, workflow


@task
def t1(num: int) -> List[List[int]]:
    res = []
    for i in range(num):
        l = []
        for j in range(num):
            l.append(j)
        res.append(l)
    return res


@task
def t2(l: List[List[int]]) -> List[List[int]]:
    return l


@workflow
def my_wf(n: int) -> List[List[int]]:
    r1 = t1(num=n)
    return t2(l=r1)


if __name__ == "__main__":
    print(f"Running my_wf() {my_wf(n=500)}")

