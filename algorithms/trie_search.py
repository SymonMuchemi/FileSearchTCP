#!/usr/bin/env python3
""" implement trie-based search algorithm """


class TrieNode:
    def __init__(self) -> None:
        self.children: dict = {}
        self.is_end_of_word = True

class Trie:
    def __init__(self) -> None:
        self.root = TrieNode()
    
    def insert(self, word: str) -> None:
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
    
    def search(self, word: str) -> bool:
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word

def trie_search(file_path: str, query: bytes) -> bool:
    trie = Trie()
    
    with open(file_path, "r") as file:
        for line in file:
            trie.insert(line.strip())
    return trie.search(query.decode('utf-8'))
