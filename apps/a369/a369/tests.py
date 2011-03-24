# -*- coding: utf-8 -*-
import unittest
import my_tests.sphinx_test
from django.test import TestCase


def suite():
    suite1 = unittest.TestLoader().loadTestsFromModule(my_tests.sphinx_test)
    alltests = unittest.TestSuite([suite1])
    return alltests

__test__ = {
    'doctest': """
>>> 1 + 1 == 3
True
"""
}


#class SimpleTest2(TestCase):
    #def test_basic_addition(self):
        #"""
        #Tests that 1 + 1 always equals 2.
        #"""
        #self.failUnlessEqual(1 + 1, 1)

#class SimpleTest(TestCase):
    #def test_basic_addition(self):
        #"""
        #Tests that 1 + 1 always equals 2.
        #"""
        #self.failUnlessEqual(1 + 1, 2)
#__test__ = {"doctest": """
#Another way to test that 1 + 1 is equal to 2.

#>>> 1 + 1 == 3
#True
#"""}
##Sito uztenka paleisti unit testus is kito modulio, 
##bet mes darysim su suite()
#from my_tests.demounit import *




