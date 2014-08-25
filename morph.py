# coding: utf-8
"""
Tiny morphology library based on Hagen Dictionary
(http://www.speakrus.ru/dict/hagen-morph.rar). Our
implementation consumes a lot of memory and returns
only lemmas but it's quite fast.
Provided 'as is' and completely free :-)

Michael Drozdovsky, 2014
michael@drozdovsky.com
"""
import sys
import pickle


class Morphology(object):
    """
    Main morphology implementation
    Dictionary is described as:
    1) Different words are separated with empty row
    2) Different forms of the same word are separated with newline
    3) First row of word description is the lemma itself
    4) Each row consists of three columns separated with tabulation.
       The first one is a word form, the next is morphological info
       and the third is word ID
    """
    def __init__(self, db_file='morph.db'):
        # search dictionary itself
        # and word forms list
        self.search_dict = {}
        self.word_forms = []

        self.db_file = db_file

    def save(self):
        # saves dict state
        werk_tuple = (self.search_dict, self.word_forms)
        with open(self.db_file, 'wb+') as f:
            pickle.dump(werk_tuple, f)

    def restore(self):
        # restores dict state
        with open(self.db_file, 'rb') as f:
            self.search_dict, self.word_forms = pickle.load(f)

    def compile(self, source_file):
        # compiles dict from Hagen Morphology file
        with open(source_file, 'r') as f:
            pq = []
            for line in f:
                word_form = line.lower().strip().split('\t')
                if len(word_form) == 3:
                    pq.append(word_form[0])
                else:
                    if pq:
                        self.word_forms.append(pq[:])
                        form_id = len(self.word_forms) - 1

                        for item in pq:
                            self.search_dict[item] = form_id
                        pq = []

        return self.search_dict

    def get_forms(self, word):
        # gets all forms of the word provided
        word = word.lower().strip()
        if word in self.search_dict:
            return self.word_forms[self.search_dict[word]]

        return None

    def get_first_form(self, word):
        # gets the first form of the word provided
        word_forms = self.get_forms(word)
        if word_forms:
            return word_forms[0]

        return None
