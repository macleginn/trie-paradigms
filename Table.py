"""A helper module that provides a function to create a co-occurrence table for
a corpus using Trie.py"""

import re
import string

import pandas as pd
from nltk.tokenize import word_tokenize

from Trie import Trie

# TODO: a better word filter
non_word_pattern = re.compile(f'(\\d|[{string.punctuation}—])+')


def corpus2table(data_path, table_path=None, testing=False):
    trie = Trie()

    with open(data_path, 'r', encoding='utf-8') as inp:
        for line in inp:
            words = word_tokenize(line)
            for w in words:
                w = non_word_pattern.sub('', w)
                if not w:
                    continue
                trie.insert(f'{w.lower()}#')
    prefix_suffix_tree = trie.get_prefix_suffix_tree()

    if testing:
        from pprint import pprint
        pprint(prefix_suffix_tree)

    d = pd.DataFrame.from_records(prefix_suffix_tree)
    d.fillna(0).transpose().astype(int).to_csv(table_path)


if __name__ == '__main__':
    corpus2table('test_data/duc.txt', 'test_data/duc.csv', False)
