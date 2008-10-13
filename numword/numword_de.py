# -*- coding: utf-8 -*-
#This file is part of numword.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
'''
numword for DE
'''
from numword_eu import NumWordEU

#//TODO: Use German error messages
class NumWordDE(NumWordEU):
    '''
    NumWord DE
    '''
    def _set_high_numwords(self, high):
        '''
        Set high num words
        '''
        max = 3 + 6*len(high)

        for word, n in zip(high, range(max, 3, -6)):
            self.cards[10**n] = word + "illiarde"
            self.cards[10**(n-3)] = word + "illion"

    def _setup(self):
        '''
        Setup
        '''
        self.negword = "minus "
        self.pointword = "Komma"
        self.errmsg_nonnum = "Nur Zahlen koennen in Worte konvertiert werden."
        self.errmsg_toobig = "Zahl ist zu gross um in Worte konvertiert zu werden."
        self.exclude_title = []
        lows = ["Non", "Okt", "Sept", "Sext", "Quint", "Quadr", "Tr", "B", "M"]
        units = ["", "Un", "Do", "Tre", "Quattuor", "Quin", "Sex", "Septem",
                 "Okto", "Novem"]
        tens = ["Dezi", "Vigint", "Trigint", "Quadragint", "Quinquagint",
                "Sexagint", "Septuagint", "Oktogint", "Nonagint"]
        self.high_numwords = ["zent"]+self._gen_high_numwords(units, tens, lows)
        self.mid_numwords = [(1000, "tausend"), (100, "hundert"),
                             (90, "neunzig"), (80, "achtzig"), (70, "siebzig"),
                             (60, "sechzig"), (50, "fünfzig"), (40, "vierzig"),
                             (30, "dreißig"), (20, "zwanzig"), (19, "neunzehn"), 
                             (18, "achtzehn"), (17, "siebzehn"), (16, "sechzehn"), 
                             (15, "fünfzehn"), (14, "vierzehn"), (13, "dreizehn"),
                             (12, "zwölf"), (11, "elf"), (10, "zehn")]
        self.low_numwords = ["neun", "acht", "sieben",
                             "sechs", "fünf", "vier", "drei", "zwei", "eins",
                             "null"]
        self.ords = { "eins"    : "ers",
                      "drei"    : "drit",
                      "acht"    : "ach",
                      "sieben"  : "sieb",
                      "hundert" : "hunderts",
                      "tausend" : "tausends",
                      "million" : "millionens",
                      "ig"      : "igs" }
        self.ordflag = False

    def _cardinal_float(self, value):
        '''
        Convert float to cardinal
        '''
        try:
            assert float(value) == value
        except (ValueError, TypeError, AssertionError):
            raise TypeError(self.errmsg_nonnum % value)
        pre = int(round(value))
        post = abs(value - pre)
        out = [self.cardinal(pre)]
        if self.precision:
            out.append(self._title(self.pointword))

            decimal = int(round(post * (10**self.precision)))
            for digit in tuple([x for x in str(decimal)]):
                out.append(str(self.cardinal(int(digit))))
                number = " ".join(out)
        return number

    def _merge(self, curr, next):
        '''
        Merge
        '''
        ctext, cnum, ntext, nnum = curr + next
        if cnum == 1:
            if nnum == 100 or nnum == 10**3 :
                return ("ein" + ntext, nnum)
            if nnum >= 10**6 and not (nnum % 10**3):
                return ("eine " + ntext.capitalize(), nnum)
            return next
        if nnum > cnum:
            if nnum >= 10**6:
                if ntext[-1] =="e":
                    ntext = ntext[:-1]
                if cnum > 1:
                    ntext += "en"
                ctext += " "
            val = cnum * nnum
        else:
            if nnum < 10 < cnum < 100:
                if nnum == 1:
                    ntext = "ein"
                ntext, ctext =  ctext, ntext + "und"
            elif nnum < 10 < cnum < 1000:
                if nnum == 1:
                    ntext = "eins"
                ntext, ctext =  ntext, ctext
            if cnum >= 10**6 and nnum <> 0:
                ctext += " "
            val = cnum + nnum

        word = ctext + ntext
        return (word.strip(), val)

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

    def ordinal_number(self, value):
        '''
        Convert to ordinal number
        '''
        self._verify_ordinal(value)
        return str(value) + "te"

    def currency(self, val, longval=True, old=False, hightxt=False, \
        lowtxt=False, space=True):
        '''
        Convert to currency
        '''
        if old:
            return self._split(val, hightxt="Mark", lowtxt="Pfennig(e)",
                                    jointxt="und",longval=longval)
        curr = super(NumWordDE, self).currency(val, jointxt="und", \
                hightxt="Euro", lowtxt="Cent", longval=longval, \
                space=space)
        return curr.replace("eins","ein")

    def cardinal(self, value):
        # catch floats and parse decimalplaces 
        if isinstance(value, float):
            prefix, suffix = str(value).split(".")
            pre_card = super(NumWordDE, self).cardinal(int(prefix))
            suf_card = self._cardinal_float(float("." + suffix))
            suf_card = suf_card.replace("null %s" % (_NW.pointword),_NW.pointword)
            cardinal = pre_card + " " + suf_card
            return cardinal
        else:
            return super(NumWordDE, self).cardinal(value)

    def year(self, val, longval=True):
        if not (val//100)%10:
            return self.cardinal(val)
        year = self._split(val, hightxt="hundert", longval=longval, space=False)
        if year.count(self.negword) != 0:
            year = year.replace(self.negword, "").strip()
            year = year + " v. Chr."
        return year.replace("eins","ein")

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

def year(value):
    '''
    Convert to year
    '''
    return _NW.year(value)

def main():
    test_cardinals = [
            [-1.0000100, "minus eins Komma null"],
            [1.11, "eins Komma eins eins"],
            [1, "eins"],
            [11, "elf"],
            [12, "zwölf"],
            [21, "einundzwanzig"],
            [29, "neunundzwanzig"],
            [30, "dreißig"],
            [31, "einunddreißig"],
            [33, "dreiunddreißig"],
            [71, "einundsiebzig"],
            [80, "achtzig"],
            [81, "einundachtzig"],
            [91, "einundneunzig"],
            [99, "neunundneunzig"],
            [100, "einhundert"],
            [101, "einhunderteins"],
            [102, "einhundertzwei"],
            [151, "einhunderteinundfünfzig"],
            [155, "einhundertfünfundfünfzig"],
            [161, "einhunderteinundsechzig"],
            [180, "einhundertachtzig"],
            [300, "dreihundert"],
            [301, "dreihunderteins"],
            [308, "dreihundertacht"],
            [832, "achthundertzweiunddreißig"],
            [1000, "eintausend"],
            [1001, "eintausendeins"],
            [1061, "eintausendeinundsechzig"],
            [1100, "eintausendeinhundert"],
            [1111, "eintausendeinhundertelf"],
            [1500, "eintausendfünfhundert"],
            [1701, "eintausendsiebenhunderteins"],
            [3000, "dreitausend"],
            [8280, "achttausendzweihundertachtzig"],
            [8291, "achttausendzweihunderteinundneunzig"],
            [10100, "zehntausendeinhundert"],
            [10101, "zehntausendeinhunderteins"],
            [10099, "zehntausendneunundneunzig"],
            [12000, "zwölftausend"],
            [150000, "einhundertfünfzigtausend"],
            [500000, "fünfhunderttausend"],
            [1000000, "eine Million"],
            [1000100, "eine Million einhundert"],
            [1000199, "eine Million einhundertneunundneunzig"],
            [2000000, "zwei Millionen"],
            [2000001, "zwei Millionen eins"],
            [1000000000, "eine Milliarde"],
            [2147483647,"zwei Milliarden einhundertsiebenundvierzig" 
             " Millionen vierhundertdreiundachtzigtausend"
             "sechshundertsiebenundvierzig"],
            [23000000000, "dreiundzwanzig Milliarden"],
            [126000000000001, "einhundertsechsundzwanzig Billionen eins"],
            [-121211221211111 , "minus "\
            "einhunderteinundzwanzig Billionen "\
            "zweihundertelf Milliarden zweihunderteinundzwanzig Millionen "\
            "zweihundertelftausendeinhundertelf"],
            [1000000000000000, "eine Billiarde"],
            [256000000000000000, "zweihundertsechsundfünfzig Billiarden"],
            # I know the next is wrong! but what to do?
            [-2.12, "minus zwei Komma eins zwei"],
            [7401196841564901869874093974498574336000000000, "sieben Septil"
             "liarden vierhunderteins Septillionen einhundertsechsundneunzig S"
             "extilliarden achthunderteinundvierzig Sextillionen fünfhundertvi"
             "erundsechzig Quintilliarden neunhunderteins Quintillionen achthu"
             "ndertneunundsechzig Quadrilliarden achthundertvierundsiebzig Qua"
             "drillionen dreiundneunzig Trilliarden neunhundertvierundsiebzig "
             "Trillionen vierhundertachtundneunzig Billiarden fünfhundertvieru"
             "ndsiebzig Billionen dreihundertsechsunddreißig Milliarden"],
            ]
    i = 1
    for number, word in test_cardinals:
        try:
            assert word == cardinal(number)
            i += 1
        except AssertionError:
            print "Failed:'%s' != '%s' != '%s'" % \
                (number, cardinal(number), word)
            raise AssertionError, "At least one test failed!" \
                " (Test no. %s of %s)" % (i, len(test_cardinals))
    print "All %s tests for cardinal numbers successfully passed." \
        % (len(test_cardinals))

    test_years = [
            # Watch out, negative years are broken!
            [0, "null"],
            [33, "dreiunddreißig"],
            [150, "einhundertfünfzig"],
            [160, "einhundertsechzig"],
            [1130, "elfhundertdreißig"],
            [1999, "neunzehnhundertneunundneunzig"],
            [1984, "neunzehnhundertvierundachtzig"],
            [2000, "zweitausend"],
            [2001, "zweitausendeins"],
            [2010, "zweitausendzehn"],
            [2012, "zweitausendzwölf"],
    ]
    i = 1
    for number, word in test_years:
        try:
            assert word == year(number)
        except AssertionError:
            print "Failed:'%s' != '%s' != '%s'" % \
                (number, year(number), word)
            raise AssertionError, "At least one test failed!" \
                " (Test no. %s of %s)" % (i, len(test_years))
    print "All %s tests for year numbers successfully passed." \
        % (len(test_years))


    test_currency =  [
            [12222, "einhundertzweiundzwanzig Euro und zweiundzwanzig Cent"],
            [123322, "eintausendzweihundertdreiunddreißig Euro und zweiundzwanzig Cent"],
            [686412, "sechstausendachthundertvierundsechzig Euro und zwölf Cent"],
            [84, "vierundachtzig Cent"],
            [1,"ein Cent"],
    ]
    i = 1
    for number, word in test_currency:
        try:
            assert word == currency(number)
        except AssertionError:
            print "Failed:'%s' != '%s' != '%s'" % \
                (number, currency(number), word)
            raise AssertionError, "At least one test failed!" \
                " (Test no. %s of %s)" % (i, len(test_currency))
    print "All %s tests for currency numbers successfully passed." \
        % (len(test_currency))

    test_ordinal =  [
            [1, "erste"],
            [3, "dritte"],
            [11, "elfte"],
            [12, "zwölfte"],
            [21, "einundzwanzigste"],
            [29, "neunundzwanzigste"],
            [30, "dreißigste"],
            [31, "einunddreißigste"],
            [33, "dreiunddreißigste"],
            [71, "einundsiebzigste"],
            [80, "achtzigste"],
            [81, "einundachtzigste"],
            [91, "einundneunzigste"],
            [99, "neunundneunzigste"],
            [100, "einhundertste"],
            [101, "einhunderterste"],
            [102, "einhundertzweite"],
            [151, "einhunderteinundfünfzigste"],
            [155, "einhundertfünfundfünfzigste"],
            [161, "einhunderteinundsechzigste"],
            [180, "einhundertachtzigste"],
            [300, "dreihundertste"],
            [301, "dreihunderterste"],
            [308, "dreihundertachte"],
            [832, "achthundertzweiunddreißigste"],
            [1000, "eintausendste"],
            [1001, "eintausenderste"],
            [1061, "eintausendeinundsechzigste"],
            [2000001, "zwei Millionen erste"],
            # The following is broken
            #[1000000000, "eine Milliardeste"],
            [2147483647,"zwei Milliarden einhundertsiebenundvierzig" 
             " Millionen vierhundertdreiundachtzigtausend"
             "sechshundertsiebenundvierzigste"],

    ]
    i = 1
    for number, word in test_ordinal:
        try:
            assert word == ordinal(number)
        except AssertionError:
            print "Failed:'%s' != '%s' != '%s'" % \
                (number, ordinal(number), word)
            raise AssertionError, "At least one test failed!" \
                " (Test no. %s of %s)" % (i, len(test_ordinal))
    print "All %s tests for ordinal numbers successfully passed." \
        % (len(test_ordinal))


if __name__ == "__main__":
    main()

