# -*- coding: utf-8 -*-
#This file is part of numword.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
'''
numword for DE
'''

from numword_eu import NumWordEU


class NumWordDE(NumWordEU):
    '''
    NumWord DE
    '''

    def __init__(self):
        self.ordflag = False
        super(NumWordDE, self).__init__()

    def _set_high_numwords(self, high):
        '''
        Set high numwords
        '''
        max_val = 3 + 6 * len(high)

        for word, i in zip(high, range(max_val, 3, -6)):
            self.cards[10**i] = word + "illiarde"
            self.cards[10**(i - 3)] = word + "illion"

    def _setup(self):
        '''
        Setup
        '''
        self.negword = "minus "
        self.pointword = "Komma"
        self.errmsg_nonnum = "Only numbers may be converted to words."
        self.errmsg_toobig = "Number is too large to convert to words."
        self.exclude_title = []

        lows = ["non", "okt", "sept", "sext", "quint", "quadr", "tr", "b", "m"]
        units = ["", "un", "duo", "tre", "quattuor", "quin", "sex", "sept",
                "okto", "novem"]
        tens = ["dez", "vigint", "trigint", "quadragint", "quinquagint",
                "sexagint", "septuagint", "oktogint", "nonagint"]
        self.high_numwords = ["zent"] + self._gen_high_numwords(
                units, tens, lows)
        self.mid_numwords = [(1000, "tausand"), (100, "hundert"),
                (90, "neunzig"), (80, "achtzig"), (70, "siebzig"),
                (60, "sechzig"), (50, "fünfzig"), (40, "vierzig"),
                (30, "dreißig")]
        self.low_numwords = ["zwanzig", "neunzehn", "achtzen", "siebzehn",
                "sechzehn", "fünfzehn", "vierzehn", "dreizehn",
                "zwölf", "elf", "zehn", "neun", "acht", "sieben",
                "sechs", "fünf", "vier", "drei", "zwei", "eins",
                "null"]
        self.ords = {"eins": "ers",
                "drei": "drit",
                "acht": "ach",
                "sieben": "sieb",
                "ig": "igs"}

    def _merge(self, curr, next):
        '''
        Merge
        '''
        ctext, cnum, ntext, nnum = curr + next

        if cnum == 1:
            if nnum < 10**6 or self.ordflag:
                return next
            ctext = "eine"

        if nnum > cnum:
            if nnum >= 10**6:
                if cnum > 1:
                    if ntext.endswith("e") or self.ordflag:
                        ntext += "s"
                    else:
                        ntext += "es"
                ctext += " "
            val = cnum * nnum
        else:
            if nnum < 10 < cnum < 100:
                if nnum == 1:
                    ntext = "ein"
                ntext, ctext =  ctext, ntext + "und"
            elif cnum >= 10**6:
                ctext += " "
            val = cnum + nnum

        word = ctext + ntext
        return (word, val)

    def ordinal(self, value):
        '''
        Convert to ordinal
        '''
        self._verify_ordinal(value)
        self.ordflag = True
        outword = self.cardinal(value)
        self.ordflag = False
        for key in self.ords:
            if outword.endswith(key):
                outword = outword[:len(outword) - len(key)] + self.ords[key]
                break
        return outword + "te"

    #XXX Is this correct??
    def ordinal_number(self, value):
        '''
        Convert to ordinal number
        '''
        self._verify_ordinal(value)
        return str(value) + "te"


    def currency(self, val, longval=True, old=False):
        '''
        Convert to currency
        '''
        if old:
            return self._split(val, hightxt="mark/s", lowtxt="pfennig/e",
                                    jointxt="und",longval=longval)
        return super(NumWordDE, self).currency(val, jointxt="und",
                                                    longval=longval)

    def year(self, val, longval=True):
        '''
        Convert to year
        '''
        if not (val//100)%10:
            return self.cardinal(val)
        return self._split(val, hightxt="hundert", longval=longval)

_NW = NumWordDE()

def cardinal(value):
    '''
    Convert to cardinal
    '''
    return _NW.cardinal(value)

def ordinal(value):
    '''
    Convert to ordinal
    '''
    return _NW.ordinal(value)

def ordinal_number(value):
    '''
    Convert to ordinal number
    '''
    return _NW.ordinal_number(value)

def currency(value, longval=True, old=False):
    '''
    Convert to currency
    '''
    return _NW.currency(value, longval=longval, old=old)

def year(value, longval=True):
    '''
    Convert to year
    '''
    return _NW.year(value, longval=longval)

def main():
    '''
    Main
    '''
    for val in [ 1, 11, 12, 21, 31, 33, 71, 80, 81, 91, 99, 100, 101, 102, 120, 155,
             180, 300, 308, 832, 1000, 1001, 1061, 1100, 1120, 1500, 1701, 1800,
             2000, 2010, 2099, 2171, 3000, 8280, 8291, 150000, 500000, 1000000,
             2000000, 2000001, -21212121211221211111, -2.121212, -1.0000100,
             1325325436067876801768700107601001012212132143210473207540327057320957032975032975093275093275093270957329057320975093272950730]:
        _NW.test(val)

if __name__ == "__main__":
    main()
