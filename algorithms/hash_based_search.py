#!/usr/bin/env python3
""" Hash based search implementation """


def hash_based_search(file_path: str, query: bytes) -> bool:
    """Performs a hash based search for a given string in a file.

    Args:
        file_path (str): The path to the file to be searched.
        query (bytes): The string to search for, encoded in bytes.

    Returns:
        bool: True if the search string is found in the file, False otherwise.
    """
    isFound = False
    key = query.decode('utf-8')

    with open(file_path, 'r') as file:
        lines = set(line.strip() for line in file)

    isFound = True if key in lines else False

    return isFound
