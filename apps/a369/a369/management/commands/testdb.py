# -*- coding: utf-8 -*-
from django.core.management.base import NoArgsCommand
import unittest
#import rpdb2
from core.models import Documents
import re

class Command(NoArgsCommand):
    help = """
    If you need Arguments, please check other modules in 
    django/core/management/commands.
    """
    def handle_noargs(self, **options):
        suite = unittest.TestLoader().loadTestsFromTestCase(TestChronology)
        unittest.TextTestRunner().run(suite)

class TestChronology(unittest.TestCase):
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def test_chonology(self):
        """
        Tests that the next results are always later than the given.
        TODO: to compare the first two values and decide wether that's
        incremental results or decremental.
        """
        result_list = Documents.searchdelta.query("adamkus").\
                    order_by('-date_birth', '@rank')

        for i in result_list:
            print i.date_birth
        
        def compare(date1, date2, type_of_comparison):
            """
            > - greaterthan, DESC, newest at the top, more, later
            < - lessthan, ASC, oldest at the top, less, earlier
            returns true if comparison is true or dates are equal
            returns false of comparison is false
            """
            assert ( type_of_comparison in ['ASC', 'DESC', None] )
            if (type_of_comparison == None):
                return True
            elif (type_of_comparison == 'ASC') and (date1<=date2):
                return True
            elif (type_of_comparison == 'DESC') and (date1>=date2):
                return True
            else:
                return False
        
        type_comp = None
        for index, item in enumerate(result_list):
            try:
                nextitem = result_list[index+1]
                #decides if the sort is ASC ir DESC, based on first two dates
                #(asuming they are in correct order), as all the next ones should
                #have the same order. If date objects are equal, we're leaving
                #setting type_comp for the next iteration
                #rpdb2.start_embedded_debugger("nx")
                if not type_comp:
                    if (item.date_birth<nextitem.date_birth):
                        global type_comp
                        type_comp = 'ASC'#pirma data yra seniau už antrą
                        print "Seniausi viršuje"

                    elif (item.date_birth>nextitem.date_birth):
                        global type_comp
                        type_comp = 'DESC'#pirma data yra anksčiau už antrą
                        print "Naujausi viršuje"

                else:
                    pass #dates are equal, will set type_comp in next iteration
                #Compares the date.
                if not compare(item.date_birth, nextitem.date_birth, type_comp):
                    print type_comp
                    print item.date_birth, item, item.nickas
                    print nextitem.date_birth, nextitem, nextitem.nickas
                    raise ArithmeticError
                else:
                    print "OK"
                
                #raise ArithmeticError
            except IndexError,AssertionError:
                pass
       
    def test_passages(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        print "in your face"
        result_list = Documents.searchdelta.query("adamkus").set_options(passages=True,passages_opts={\
                                       'before_match':"<em>",\
                                       'after_match':'</em>',\
                                       'chunk_separator':' ... ',\
                                       'around':6,\
                                       'limit':50000,\
                                    })
        pattern = re.compile('.*em.*')#em.*')#\<em\>.*')#\</em\>.*')
        for result in result_list:
            print "naujas_objektas"
            exists_em = False
            passages_dict = result.sphinx.get('passages')
            for k in passages_dict:
                if pattern.match(passages_dict.get(k)):
                    exists_em = True
            assert(exists_em)
 