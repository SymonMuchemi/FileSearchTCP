#!/usr/bin/env python3
""" Naive line-by-line search algorithm implementation """


from typing import Any, Generator


def read_file_generator(file_path: str) -> Generator[str, Any, None]:
    with open(file_path, 'r') as file:
        for line in file:
            yield line.strip()


def naive_search(file_path: str, search_sting: str) -> bool:
    for line in read_file_generator(file_path):
        if line == search_sting:
            return True
    return False
