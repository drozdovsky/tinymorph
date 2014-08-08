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
    def __init__(self, source_file=None, db_file='morph.db'):
        self.ref_dict = {}
        self.first_forms = []
        self.source_file = source_file
        self.db_file = db_file

    def save(self):
        # сохраняем состояние словаря
        werk_tuple = (self.ref_dict, self.first_forms)
        with open(self.db_file, 'wb+') as f:
            pickle.dump(werk_tuple, f)

    def restore(self):
        # восстанавливаем состояние словаря
        with open(self.db_file, 'rb') as f:
            self.ref_dict, self.first_forms = pickle.load(f)

    def compile(self):
        # формируем dict из исходного файла
        with open(self.source_file, 'r') as f:
            pq = []
            for line in f:
                word_form = line.lower().strip().split('\t')
                if len(word_form) == 3:
                    pq.append(word_form[0])
                else:
                    if pq:
                        self.first_forms.append(pq[0])
                        form_id = len(self.first_forms) - 1

                        for item in pq:
                            self.ref_dict[item] = form_id
                        pq = []
        return self.ref_dict

    def get_form(self, word):
        # получаем начальную форму по слову
        word = word.lower().strip()
        if word in self.ref_dict:
            return self.first_forms[self.ref_dict[word]]
        return None
