# -*- coding: utf-8 -*-
import sys, re, fileinput, os, subprocess, commands, datetime
from django.core.management.base import BaseCommand
from core.models import Documents
from optparse import OptionParser, make_option

class Command(BaseCommand):
    """
    A class Command in a custom-command's module is a must.
    """
    help = "Prints hello world"
    args = '[various KEY=val options, use `runfcgi help` for help]'  
    
    def handle(self, *args, **options):
        print a
        """
        A must-be-inplemented method, which is launched fist.
        """
        option_list = BaseCommand.option_list + (
        make_option("-o", "--source_meta", dest="source_metadata",\
                    default=1),
        )