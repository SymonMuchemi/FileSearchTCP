#!/usr/bin/env python3
""" implement trie-based search algorithm """


class TrieNode:
    """A node in the Trie data structure.
    
    Attributes:
        children (dict): A dictionary containing the children of the node.
        is_end_of_word (bool): A flag to indicate the end of a word.
    """
    def __init__(self) -> None:
        """Initializes a TrieNode object."""
        self.children: dict = {}
        self.is_end_of_word: bool = True


class Trie:
    """A Trie data structure.
    
    Attributes:
        root (TrieNode): The root node of the Trie.
    """
    def __init__(self) -> None:
        """Initializes a Trie object."""
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        """Inserts a word into the Trie.
        
        Args:
            word (str): The word to be inserted.
        """
        # Start at the root node
        node = self.root
        
        # Traverse the Trie to insert the word
        for char in word:
            # Create a new node if the character is not in node.children
            if char not in node.children:
                # Add the character to the children of the node
                node.children[char] = TrieNode()
            # Move to the next node
            node = node.children[char]
        # Mark the end of the word
        node.is_end_of_word = True

    def search(self, word: str) -> bool:
        """Searches for a word in the Trie.
        
        Args:
            word (str): The word to search for.
        
        Returns:
            bool: True if the word is found in the Trie, False otherwise.
        """
        node = self.root
        
        # Traverse the Trie to find the word
        for char in word:
            # Check if th character is in the children of the node
            if char not in node.children: # return False if not found
                return False
            # Move to the next node
            node = node.children[char]
        
        # Return True if the end of the word is reached
        return node.is_end_of_word


def trie_search(file_path: str, query: bytes) -> bool:
    """
    Searches for a query string in a file using a Trie data structure.
    Args:
        file_path (str): The path to the file to be searched.
        query (bytes): The query string to search for, encoded as bytes.
    Returns:
        bool: True if the query string is found in the file, False otherwise.
    """
    # Create a Trie object
    trie: Trie = Trie()

    # Open the file in read mode
    with open(file_path, "r") as file:
        # Insert each line from the file into the Trie
        for line in file:
            trie.insert(line.strip())
    
    # Search for the query string in the Trie
    return trie.search(query.decode('utf-8'))
