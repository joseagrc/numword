# -*- coding: utf-8 -*-
#This file is part of numword.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
'''
numword for FR
'''

from numword_eu import NumWordEU


class NumWordFR(NumWordEU):
    '''
    NumWord FR
    '''

    def _setup(self):
        '''
        Setup
        '''
        self.negword = "moins "
        self.pointword = "virgule"
        self.errmsg_nonnum = "Only numbers may be converted to words."
        self.errmsg_toobig = "Number is too large to convert to words."
        self.exclude_title = ["et", "virgule", "moins"]
        self.mid_numwords = [(1000, "mille"), (100, "cent"),
                             (80, "quatre-vingts"), (60, "soixante"),
                             (50, "cinquante"), (40, "quarante"),
                             (30, "trente")]
        self.low_numwords = ["vingt", "dix-neuf", "dix-huit", "dix-sept",
                             "seize", "quinze", "quatorze", "treize", "douze",
                             "onze", "dix", "neuf", "huit", "sept", "six",
                             "cinq", "quatre", "trois", "deux", "un", "z\xE8ro"]

    def _merge(self, curr, next):
        '''
        Merge
        '''
        ctext, cnum, ntext, nnum = curr + next

        if cnum == 1:
            if nnum < 1000000:
                return next
        else:
            if (not (cnum - 80)%100 or not cnum%100) and nnum < 1000000 \
                    and ctext[-1] == "s":
                ctext = ctext[:-1]
            if (cnum < 1000 and nnum != 1000 and ntext[-1] != "s"
            and not nnum%100):
                ntext += "s"

        if nnum < cnum < 100 \
                and nnum % 10 == 1 and cnum != 80:
            return ("%s-et-%s"%(ctext, ntext), cnum + nnum)
        if nnum >= 1000000 or cnum >= 1000000:
            return ("%s %s"%(ctext, ntext), cnum + nnum)
        return ("%s-%s"%(ctext, ntext), cnum + nnum)


    def ordinal(self, value):
        '''
        Convert to ordinal
        '''
        self._verify_ordinal(value)
        if value == 1:
            return "premier"
        word = self.cardinal(value)
        if word[-1] == "e" or word[-1] == "s":
            word = word[:-1]
        if word[-1] == "f":
            word = word[:-1] + 'v'
        return word + "i\xE8me"


    def ordinal_number(self, value):
        '''
        Convert to ordinal number
        '''
        self._verify_ordinal(value)
        out = str(value)
        out +=  {"1" : "er" }.get(out[-1], "me")
        return out

    def currency(self, val, longval=True, old=False):
        '''
        Convert to currency
        '''
        hightxt = "Euro/s"
        if old:
            hightxt = "franc/s"
        return self._split(val, hightxt=hightxt, lowtxt="centime/s",
                jointxt="et", longval=longval)

_NW = NumWordFR()

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

def year(value):
    '''
    Convert to year
    '''
    return _NW.year(value)

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
