# -*- coding: utf-8 -*-
#This file is part of numword.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.

from unittest import TestCase


class TestNumWordFR(TestCase):

    def test_cardinal(self):
        from numword.numword_fr import cardinal
        self.assertEqual(cardinal(0), u"zéro")
        self.assertEqual(cardinal(11.96), u"onze virgule quatre-vingt-seize")
        self.assertEqual(cardinal(100), u"cent")
        self.assertEqual(cardinal(100.0), u"cent")
        self.assertEqual(cardinal(121.01), u"cent-vingt-et-un virgule un")
        self.assertEqual(cardinal(3121.45),
                         u"trois-mille-cent-vingt-et-un virgule quarante-cinq")

    def test_cardinal_not_a_number(self):
        from numword.numword_fr import cardinal
        error = u"type\(Ximinez\) not in \[long, int, float\]"
        with self.assertRaisesRegexp(TypeError, error):
            cardinal('Ximinez')

    def test_cardinal_number_too_big(self):
        from numword.numword_fr import cardinal
        from numword.numword_fr import NumWordFR
        max_val = NumWordFR().maxval
        number = max_val + 1
        error = u"abs\(%s\) must be less than %s" % (number, max_val)
        with self.assertRaisesRegexp(OverflowError, error):
            cardinal(number)


class TestNumWordFR_BE(TestCase):

    def test_cardinal(self):
        from numword.numword_fr_be import cardinal
        self.assertEqual(cardinal(72), u"septante-deux")
        self.assertEqual(cardinal(94), u"nonante-quatre")
        self.assertEqual(cardinal(93.79),
                         u"nonante-trois virgule septante-neuf")


class TestNumWordEN(TestCase):

    def test_cardinal(self):
        from numword.numword_en import cardinal
        self.assertEqual(cardinal(11.96), u"eleven point ninety-six")
        self.assertEqual(cardinal(100), "one hundred")
        self.assertEqual(cardinal(100.0), "one hundred")
        self.assertEqual(cardinal(121.01),
                         "one hundred and twenty-one point one")
        self.assertEqual(cardinal(3121.45),
                         u"three thousand, one hundred and twenty-one point forty-five")

    def test_cardinal_not_a_number(self):
        from numword.numword_fr import cardinal
        error = u"type\(Ximinez\) not in \[long, int, float\]"
        with self.assertRaisesRegexp(TypeError, error):
            cardinal('Ximinez')

    def test_cardinal_number_too_big(self):
        from numword.numword_fr import cardinal
        from numword.numword_fr import NumWordFR
        max_val = NumWordFR().maxval
        number = max_val + 1
        error = u"abs\(%s\) must be less than %s" % (number, max_val)
        with self.assertRaisesRegexp(OverflowError, error):
            cardinal(number)
