"""An implementation of the trie data structure with a non-standard API intended for morphonological analysis."""

from LinkedList import LinkedList


class TrieNode:
    def __init__(self, value=0):
        self.value: int = value           # Prefix count
        self.children: LinkedList = LinkedList() # The list's API ensures lexicographical order


class Trie:
    """A recursive trie with linked lists of character-indexed children.
    The root's value contains the number of words in the corpus."""

    def __init__(self):
        self.root: TrieNode = TrieNode()


    def __insert_rec(self, current_node: TrieNode, s: str):
        current_node.value += 1
        if not s:
            return
        key = s[0]
        subtrie = current_node.children.getByKey(key)
        if subtrie is None:
            new_subtrie = TrieNode()
            current_node.children.insertByKey(key, new_subtrie)
            self.__insert_rec(new_subtrie, s[1:])
        else:
            self.__insert_rec(subtrie, s[1:])


    def insert(self, s: str):
        if not s:
            return
        self.__insert_rec(self.root, s)


    def __print(self, node, stack, offset):
        """If we see a branching prefix, print the non-branching part,
        increase the offset, dump the stack."""

        # TODO: add whitespace before counts

        if node.children.size > 1:
            if stack:
                print('.' * offset + ''.join(stack) + f' {node.value}')
            for k in node.children.keys():
                self.__print(node.children.getByKey(k), [k], offset + len(stack))
        elif node.children.size == 1:
            stack.append(node.children.head.key)
            self.__print(node.children.head.value, stack, offset)
            stack.pop()
        else:
            print('.' * offset + ''.join(stack) + f' {node.value}')


    def print(self):
        self.__print(self.root, [], 0)


    def __get_token_counts_rec(self, node: TrieNode, stack, result):
        if node.children.size == 0:
            key = ''.join(stack[:-1]) # strip the end-of-word symbol
            result[key] = node.value
        else:
            for key in node.children.keys():
                stack.append(key)
                self.__get_token_counts_rec(node.children.getByKey(key), stack, result)
                stack.pop()


    def get_token_counts(self):
        result = {}
        self.__get_token_counts_rec(self.root, [], result)
        return result


    def __get_branching_prefix_counts_rec(self, node: TrieNode, stack, result):
        # TODO: eliminate the stack check by adding a loop to the API caller
        if stack and node.children.size > 1: # ignore the root node
            key = ''.join(stack)  # no end-of-word symbol!
            result[key] = node.value
        for key in node.children.keys():
            stack.append(key)
            self.__get_branching_prefix_counts_rec(node.children.getByKey(key), stack, result)
            stack.pop()


    def get_branching_prefix_counts(self):
        result = {}
        self.__get_branching_prefix_counts_rec(self.root, [], result)
        return result


    def __get_prefix_suffix_tree_rec(self, node: TrieNode, stack, result):
        if node.children.size > 1:
            # This is a branching prefix, add counts
            prefix_dict = {}
            self.__get_token_counts_rec(node, [], prefix_dict)
            result[''.join(stack)] = prefix_dict
        for k in node.children.keys():
            stack.append(k)
            self.__get_prefix_suffix_tree_rec(node.children.getByKey(k), stack, result)
            stack.pop()


    def get_prefix_suffix_tree(self):
        """The main function: returns counts of suffixes for all branching
        prefixes as a dict of dicts."""
        result = {}
        for k in self.root.children.keys(): # a loop to eliminate the check for an empty stack in the inner loop
            child = self.root.children.getByKey(k)
            self.__get_prefix_suffix_tree_rec(child, [k], result)
        return result


if __name__ == '__main__':
    from random import shuffle

    # Token-counts test
    t = Trie()
    types = [
        'cat',
        'fat',
        'hat',
        'rat'
    ]
    tokens = types * 5
    for tok in tokens:
        t.insert(tok + '#')
    result = {
        'cat': 5,
        'fat': 5,
        'hat': 5,
        'rat': 5
    }
    token_counts = t.get_token_counts()
    test_result = {
        k: token_counts[k] for k in types
    }
    assert test_result == result
    assert t.get_branching_prefix_counts() == {} # no branching prefixes here

    # Branching-prefixes test
    t = Trie()
    tokens = [
        'cat',
        'car',
        'call',
        'caledonian',
        'calling',
        'come',
        'dawn',
        'damn',
        'drill',
        'dry'
    ]
    for tok in tokens:
        t.insert(tok + '#')
    # t.print()
    assert t.get_branching_prefix_counts() == {'c': 6, 'ca': 5, 'cal': 3, 'call': 2, 'd': 4, 'da': 2, 'dr': 2}
    from pprint import pprint
    pprint(t.get_prefix_suffix_tree())