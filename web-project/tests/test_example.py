#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

import unittest


class TestStringMethods(unittest.TestCase):

    """Test Example"""

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)


def suite():
    """
        Test suite
    """
    suite = unittest.TestSuite()
    suite.addTest(TestStringMethods("test_upper"))
    suite.addTest(TestStringMethods("test_isupper"))
    suite.addTest(TestStringMethods("test_split"))
    return suite

if __name__ == "__main__":
    unittest.main(defaultTest='suite')
