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
import os
import sys
import pickle
import random


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


class Synonymizer(Morphology):
    """
    Morphology-based synonymizer implementation
    """
    def __init__(self, *args, **kwargs):
        super(Synonymizer, self).__init__(*args, **kwargs)

        self.synonym_refs = {}
        self.rnd = random.seed(os.urandom(128))

    def compile_synonyms(self, source_file):
        # создаем словарь синонимов
        with open(source_file, 'r') as f:
            for line in f:
                try:
                    word, synonym = line.lower().strip().split('\t')
                    if word not in self.search_dict:
                        continue

                    if synonym not in self.search_dict:
                        continue

                    w_ref = self.search_dict[word]
                    s_ref = self.search_dict[synonym]

                    if w_ref not in self.synonym_refs:
                        self.synonym_refs[w_ref] = []

                    if s_ref not in self.synonym_refs:
                        self.synonym_refs[s_ref] = []

                    self.synonym_refs[w_ref].append(s_ref)
                    self.synonym_refs[s_ref].append(w_ref)
                except ValueError:
                    break

    def synonymize_me(self, word):
        # синонимизируем слово
        #import pdb; pdb.set_trace()
        word = word.lower().strip()

        if word not in self.search_dict:
            return None

        word_id = self.search_dict[word]
        synonyms = self.synonym_refs.get(word_id)

        if not synonyms:
            return None

        r_syn = random.sample(synonyms, 1)[0]
        r_word = self.word_forms[r_syn]

        ret_word = r_word[0]

        # берем форму в нужном виде
        source_word = self.word_forms[word_id]
        for i, val in enumerate(source_word):
            if val == word:
                ret_word = r_word[i]
                break


        print(ret_word)
        return

        wordforms = self.get_forms(word)

        if not wordforms:
            return None

        # ищем синонимы
        synonyms = self.search_dict[word]

        word_index = None
        for i, val in enumerate(wordforms):
            if val == word:
                word_index = i
                break



if __name__ == '__main__':
    snzr = Synonymizer()
    snzr.compile('paradigms.txt')
    snzr.compile_synonyms('russian.big.syn')
    snzr.synonymize_me('палкой')
    print('FA')
