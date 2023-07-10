import random
import time
import os

from const import *


class Wordlist:

    def __init__(self):
        self.dicts = {}
        self.sort = 'l'
        self.lang = None

        self.import_dicts()


    def import_dicts(self):
        try:
            for d in random.sample(os.listdir(PATH), len(os.listdir(PATH))):
                if not d.endswith(FILE_SUFF): continue
                print(f'Importing {d}...', end='')
                start_time = time.time()
                language = d.removesuffix(FILE_SUFF)
                with open(PATH + d, 'r') as f:
                    self.dicts[language] = set()
                    for word in f.read().split('\n'):
                        if word == '' or ' ' in word:
                            continue
                        self.dicts[language].add(word)
                print(f' ({int((time.time() - start_time) * 1000)}ms)')
        except Exception as e:
            print('Error importing languages')
            raise ImportError(e)
        if not len(self.dicts):
            raise ImportError('Can\' find any language')


    def get_word(self, chars, remove=True) -> tuple:
        if self.lang is None:
            raise Exception('Language not set')
        st_tm = time.time()
        ans = None
        n = 0
        if self.sort == None:
            for word in self.dicts[self.lang]:
                if chars in word:
                    if ans is None: ans = word
                    n += 1
        elif self.sort == 'l':
            ans = ''
            for word in self.dicts[self.lang]:
                if chars in word:
                    if len(word) > len(ans):
                        ans = word
                    n += 1
        elif self.sort == 's':
            ans = 30 * '_'
            for word in self.dicts[self.lang]:
                if chars in word:
                    if len(word) < len(ans):
                        ans = word
                    n += 1
        if n:
            if remove:
                self.remove_word(ans)
            return ans, n, round((time.time() - st_tm) * 1000, 2)
        return None, 0, round((time.time() - st_tm) * 1000, 2)


    def remove_word(self, word):
        self.dicts[self.lang].remove(word)

