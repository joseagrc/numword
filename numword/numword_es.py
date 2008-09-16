#This file is part of numword.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
'''
numword for ES
'''

from numword_eu import NumWordEU

#TODO correct orthographics
#TODO error messages


class NumWordES(NumWordEU):
    '''
    NumWord ES
    '''

    def __init__(self):
        super(NumWordES, self).__init__()
        self.gender_stem = ''

    #TODO Is this sufficient??
    def _set_high_numwords(self, high):
        '''
        Set high numwords
        '''
        max_val = 3 + 6*len(high)

        for word, i in zip(high, range(max_val, 3, -6)):
            self.cards[10**(i - 3)] = word + "ill\xf2n"


    def _setup(self):
        '''
        Setup
        '''
        lows = ["cuatr", "tr", "b", "m"]
        self.high_numwords = self._gen_high_numwords([], [], lows)
        self.negword = "menos "
        self.pointword = "punto"
        self.errmsg_nonnum = "Only numbers may be converted to words."
        self.errmsg_toobig = "Number is too large to convert to words."
        self.gender_stem = "o"
        self.exclude_title = ["y", "menos", "punto"]
        self.mid_numwords = [(1000, "mil"), (100, "cien"), (90, "noventa"),
                             (80, "ochenta"), (70, "setenta"), (60, "sesenta"),
                             (50,"cincuenta"), (40,"cuarenta")]
        self.low_numwords = ["vientinueve", "vientiocho", "vientisiete",
                             "vientis\xE8is", "vienticinco", "vienticuatro",
                             "vientitr\xE8s", "vientid\xF2s", "vientiuno",
                             "viente", "diecinueve", "dieciocho", "diecisiete",
                             "dieciseis", "quince", "catorce", "trece", "doce",
                             "once", "diez", "nueve", "ocho", "siete", "seis",
                             "cinco", "cuatro", "tres", "dos", "uno", "cero"]
        self.ords = { 1  : "primer",
                      2  : "segund",
                      3  : "tercer",
                      4  : "cuart",
                      5  : "quint",
                      6  : "sext",
                      7  : "s\xE8ptim",
                      8  : "octav",
                      9  : "noven",
                      10 : "d\xE8cim" }


    def _merge(self, curr, next):
        '''
        Merge
        '''
        ctext, cnum, ntext, nnum = curr + next

        if cnum == 1:
            if nnum < 1000000:
                return next
            ctext = "un"
        elif cnum == 100:
            ctext += "t" + self.gender_stem

        if nnum < cnum:
            if cnum < 100:
                return ("%s y %s"%(ctext, ntext), cnum + nnum)
            return ("%s %s"%(ctext, ntext), cnum + nnum)
        elif (not nnum % 1000000) and cnum > 1:
            ntext = ntext[:-3] + "ones"

        if nnum == 100:
            if cnum == 5:
                ctext = "quinien"
                ntext = ""
            elif cnum == 7:
                ctext = "sete"
            elif cnum == 9:
                ctext = "nove"
            ntext += "t" + self.gender_stem + "s"
        else:
            ntext = " " + ntext

        return (ctext + ntext, cnum * nnum)


    def ordinal(self, value):
        '''
        Convert to ordinal
        '''
        self._verify_ordinal(value)
        try:
            return self.ords[value] + self.gender_stem
        except KeyError:
            return self.cardinal(value)

    def ordinal_number(self, value):
        '''
        Convert to ordinal number
        '''
        self._verify_ordinal(value)
        # Correct for fem?
        return "%s\xB0" % value


    def currency(self, val, longval=True, old=False):
        '''
        Convert to currency
        '''
        if old:
            return self._split(val, hightxt="peso/s", lowtxt="peseta/s",
                    divisor=1000, jointxt="y", longval=longval)
        return super(NumWordES, self).currency(val, jointxt="y",
                    longval=longval)

_NW = NumWordES()

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
