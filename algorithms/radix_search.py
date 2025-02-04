#!/usr/bin/env python3
""" Implements a radix search algorithm """


class RadixNode:
    """ Node class for the radix tree

    Attributes:
        children (dict): A dictionary of children nodes
        is_end_of_word (bool): Marks the end of a full line
    """
    def __init__(self) -> None:
        """ Initializes the node with an empty dictionary of children """
        self.children: dict = {}
        self.is_end_of_word = False  # Marks the end of a full line

class RadixTree:
    """ Radix tree class for searching lines

    Attributes:
        root (RadixNode): The root node of the radix tree
    """
    def __init__(self) -> None:
        """ Initializes the radix tree with an empty root node """
        self.root = RadixNode()

    def insert(self, line) -> None:
        """ Inserts a line into the radix tree """
        node = self.root

        # Traverse the tree and insert each character
        for char in line:
            # Create a new node if the character is not in the children
            if char not in node.children:
                node.children[char] = RadixNode()  # Create a new node
            node = node.children[char]  # Move to the next node
        node.is_end_of_word = True  # Mark the end of the line

    def search(self, query) -> bool:
        """ Searches for an exact match of the query.

        args:
            query (str): The query to search for
        """
        node = self.root

        # Traverse the tree and search for each character
        for char in query:
            if char not in node.children:
                return False
            # Move to the next node
            node = node.children[char]
        return True if node.is_end_of_word else False


def radix_search(filename: str, query: bytes) -> bool:
    """
    Perform a search for a query string in a file using a radix tree.
    This function reads the contents of a file, inserts each line into a radix tree,
    and then searches for the specified query string within the radix tree.
    Args:
        filename (str): The path to the file to be searched.
        query (bytes): The query string to search for, provided as bytes.
    Returns:
        bool: True if the query string is found in the file, False otherwise.
    """

    radix_tree = RadixTree()

    # Read file and insert lines into the radix tree
    with open(filename, "r") as file:
        for line in file:
            radix_tree.insert(line.strip())  # Strip to avoid newline mismatches

    # Search for the query
    return radix_tree.search(query.decode('utf-8'))
