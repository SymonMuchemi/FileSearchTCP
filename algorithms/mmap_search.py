#!/usr/bin/env python3
""" mmap search implementation """


import mmap


def mmap_search(file_path: str, query: bytes) -> bool:
    """Searches for a byte string within a file using memory-mapped file I/O.
    Args:
        file_path (str): The path to the file to be searched.
        query (bytes): The byte string to search for within the file.
    Returns:
        bool: True if the byte string is found, False otherwise.
    """
    # Open the file in read-only mode
    with open(file_path, 'rb', buffering=0) as file:
        # create a memory-mapped file object
        m = mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ)

        # search for the query string in the memory-mapped file
        if m.find(query) != -1:
            print(f'Found the string: {query!r}')
            return True
        return False
