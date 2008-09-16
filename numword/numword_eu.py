#This file is part of numword.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
'''
numword for EU
'''

from numword_base import NumWordBase

class NumWordEU(NumWordBase):
    '''
    NumWord EU
    '''

    def _set_high_numwords(self, high):
        '''
        Set high num words
        '''
        max_val = 3 + 6 * len(high)

        for word, i in zip(high, range(max_val, 3, -6)):
            self.cards[10**i] = word + "illiard"
            self.cards[10**(i-3)] = word + "illion"

    def _base_setup(self):
        '''
        Base setup
        '''
        lows = ["non", "oct", "sept", "sext", "quint", "quadr", "tr", "b", "m"]
        units = ["", "un", "duo", "tre", "quattuor", "quin", "sex", "sept",
                 "octo", "novem"]
        tens = ["dec", "vigint", "trigint", "quadragint", "quinquagint",
                "sexagint", "septuagint", "octogint", "nonagint"]
        self.high_numwords = ["cent"] + self._gen_high_numwords(units, tens, lows)

    def currency(self, value, longval=True, jointxt=""):
        '''
        Convert to currency
        '''
        return self._split(value, hightxt="Euro/s", lowtxt="Euro cent/s",
                                jointxt=jointxt, longval=longval)

    def _merge(self, curr, next):
        '''
        Merge
        '''
        raise NotImplementedError
