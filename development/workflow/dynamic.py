import typing
from time import sleep

from flytekit import dynamic, task, workflow


@task
def return_index(character: str) -> int:
    """
    Computes the character index (which needs to fit into the 26 characters list)"""
    sleep(1)
    if character.islower():
        return ord(character) - ord("a")
    else:
        return ord(character) - ord("A")


@task
def update_list(freq_list: typing.List[int], list_index: int) -> typing.List[int]:
    """
    Notes the frequency of characters"""
    freq_list[list_index] += 1
    return freq_list


@task
def derive_count(freq1: typing.List[int], freq2: typing.List[int]) -> int:
    """
    Derives the number of common characters"""
    count = 0
    for i in range(26):
        count += min(freq1[i], freq2[i])
    return count


@dynamic
def count_characters(s1: str, s2: str) -> int:
    """
    Calls the required tasks and returns the final result"""

    # s1 and s2 are accessible

    # initializing an empty list consisting of 26 empty slots corresponding to every alphabet (lower and upper case)
    freq1 = [0] * 26
    freq2 = [0] * 26

    # looping through the string s1
    for i in range(len(s1)):
        # index and freq1 are not accessible as they are promises
        index = return_index(character=s1[i])
        freq1 = update_list(freq_list=freq1, list_index=index)

    # looping through the string s2
    for i in range(len(s2)):
        # index and freq2 are not accessible as they are promises
        index = return_index(character=s2[i])
        freq2 = update_list(freq_list=freq2, list_index=index)

    # counting the common characters
    return derive_count(freq1=freq1, freq2=freq2)


@workflow
def wf(s1: str = "Pear", s2: str = "Earth") -> int:
    """
    Calls the dynamic workflow and returns the result"""

    # sending two strings to the workflow
    return count_characters(s1=s1, s2=s2)


if __name__ == "__main__":
    print(wf(s1="Pear", s2="Earth"))
