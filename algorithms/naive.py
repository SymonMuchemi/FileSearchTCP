#!/usr/bin/env python3
""" Naive line-by-line search algorithm implementation """


from typing import Any, Generator


def read_file_generator(file_path: str) -> Generator[str, Any, None]:
    """
    A generator function that reads a file line by line and yields each line
    stripped of leading and trailing whitespace.

    Args:
        file_path (str): The path to the file to be read.
    Yields:
        str: A line from the file, stripped of leading and trailing whitespace.
    """

    with open(file_path, 'r') as file:
        for line in file:
            yield line.strip()


def naive_search(file_path: str, search_sting: bytes) -> bool:
    """
    Perform a naive search for a given string in a file.
    Args:
        file_path (str): The path to the file to be searched.
        search_sting (bytes): The string to search for, encoded in bytes.
    Returns:
        bool: True if the search string is found in the file, False otherwise.
    """

    search_key: str = search_sting.decode('utf-8')

    for line in read_file_generator(file_path):
        if line == search_key:
            return True
    return False
