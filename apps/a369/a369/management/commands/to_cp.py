# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from core.models import Documents
from optparse import OptionParser, make_option
#import re
#import rpdb2
import wingdbstub
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
        
        """
        parsinam argsus
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
        
        """
        rašom į failą
        """
        file_to_write = open(self.output,"w")
        i = 0
        for line in fileinput.input(self.input):
            file_to_write.write(line)
            i +=1
            if (i % 2) == 0:
                print i
                sys.exit(2)
             
        """
        SQLAlchemy
        printinam stulpelius
        """
        table_columns = []
        from sqlalchemy import *
        from sqlalchemy.orm import *
        conn_row = "mysql://%s:%s@%s/%s?use_unicode=1&charset=utf8" %\
                 ()
        
        db = create_engine(conn_row)
        #try:
            #file_to_read = open(self.input,"r")
        #except:
            #print "nepavyko atidaryti skaitymo failo"
        #try:
            #file_to_write = open(self.output,"w")
        #except:
            #print "nepavyko atidaryti rašymo failo"
        #for i in range(10):
            #try:
                #print file_to_read.readline(i)
            #except:
                #print "atrodo failo galas"
                #sys.exit(2) 
                
        
            
            
        #self.parse_options()
        #self.cp_files()
        
    #def cp_files(self):
        #try:
            #file_to_read = open(self.input,"r")
        #except:
            #print "nepavyko atidaryti skaitymo failo"
        #try:
            #file_to_write = open(self.output,"w")
        #except:
            #print "nepavyko atidaryti skaitymo failo"
        #for i in range(1000):
            #try:
                #print file_to_read.readline(i)
            #except:
                #print "atrodo failo galas"
                #sys.exit(2) 

        
        
    #def parse_options(self):
        #"""
        #Parse options, set instance variables.
        #"""

            
        
            
    
            
                        
        
        
        