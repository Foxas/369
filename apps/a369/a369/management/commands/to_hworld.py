# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from core.models import Documents
from optparse import OptionParser, make_option

#import re
#import rpdb2
import sys
import fileinput




class Command(BaseCommand):
    """
    A class Command in a custom-command's module is a must.
    """
    help = "Prints hello world"
    args = '[various KEY=val options, use `runfcgi help` for help]'
    input = ""
    output = ""
    
    option_list = BaseCommand.option_list + (
        make_option("-i", "--input", dest="input",),# default="/var/input"),
        make_option("-o", "--output", dest="output",),# default="/var/output"),
    )
    
    def handle(self, *args, **options):
        """
        A must-be-inplemented method, which is launched fist.
        """
        try:
            self.input, self.output = options["input"], options["output"]
        except:
            print "Erroras"
        if not self.input or not self.output:
            print "not enough arguments"
            SystemExit()
        else:
            print self.input, self.output
        

                        
        
        
        