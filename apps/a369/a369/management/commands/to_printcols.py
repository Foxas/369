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
        """
        A must-be-inplemented method, which is launched fist.
        """
        import settings
        print "i am in a class"

"""
TODO
-make all the field/line termination symbols as a settings
"""

#script settings
fields_terminated_by = ";...;"
fields_enclosed_by = ""
fields_escaped_by = "\\\\"
lines_terminated_by = "\n"
lines_starting_by = ""

        
import settings
from core.models import Documents
db_engine = settings.DATABASE_ENGINE
db_name = settings.DATABASE_NAME
db_pass = settings.DATABASE_PASSWORD
db_port = settings.DATABASE_PORT
db_user = settings.DATABASE_USER
db_table_name = Documents._meta.db_table
db_socket = "/home/toinbis/Desktop/programming/369/runtime/var/pids/mysql.sock"

db_conn_row = "%s://%s:%s@localhost:%s/%s?use_unicode=1&charset=utf8&unix_socket=%s"\
       % (db_engine,db_user,db_pass, db_port, db_name, db_socket)

print db_conn_row

from sqlalchemy import *
from sqlalchemy.orm import *


db = create_engine(db_conn_row)
db_md = MetaData()
db_md.bind = db
db_table_documents = Table("documents",db_md,autoload=True)
class DbDocs(object)	:
    pass
mapper(DbDocs,db_table_documents)



#======
#SELECT * INTO OUTFILE (aka source DB). sita veliau darysim, dbu importinam
#sugeneruota failiuka tiesiog
#=======
db_engine2 = 'mysql'
db_name2 = 'kpw'
db_pass2 = settings.DATABASE_PASSWORD
db_port2 = '3306'
db_user2 = 'Sml711'
db_socket2 = "/var/run/mysqld/mysqld.sock"

db_conn_row2 = "%s://%s:%s@localhost:%s/%s?use_unicode=1&charset=utf8unix_socket=%s"\
       % (db_engine2,db_user2,db_pass2, db_port2, db_name2, db_socket2 )
print db_conn_row2
db2 = create_engine(db_conn_row2)
db_md2 = MetaData()
db_md2.bind = db2
Session2 = sessionmaker(bind=db2)
session2 = Session()

#Load data into outfile
print "============"
print "nu tuoj select * into outfile darysi,"
output_filename2 = "/home/toinbis/Desktop/programming/369/runtime/mysql_datadir/django/pyout2.txt"



load_outfile_start_time = datetime.datetime.now()

#FIELDS TERMINATED BY '%s' ENCLOSED BY '%s' ESCAPED BY '%s'
#LINES TERMINATED BY '%s' STARTING BY '%s'

load_outfile_line=\
"""SELECT * INTO OUTFILE '%s' 
FROM TABLE kpw.documents LIMIT 10;
""" % (output_filename2,)

print load_outfile_line
session.execute(load_outfile_line)
session.commit()

skirtums = datetime.datetime.now()-load_infile_start_time
print "pradejom- %s, baigem - %s, uztrukom - %s" % (str(load_infile_start_time),str(datetime.datetime.now()),str(skirtums))
print "============"
#============

#=========

tempmd = MetaData()

types = [col.type for col in db_table_documents.columns]
for t in types:
    print t
print "aha"

for c in db_table_documents.c:
    print c.name

#Generate file
print "============"
print "Generuosim faila"
generate_file_start_time = datetime.datetime.now()

#input/output filenames
#open_filename = "/home/toinbis/Desktop/desktop_old/longread"
output_filename = "/home/toinbis/Desktop/programming/369/runtime/mysql_datadir/django/pyout.txt"


#trying to open files for reading/writing


#no need to open reading file. it's open by fileinput!
try:
    file_to_read = open(open_filename,"r")
except:
    print "nepavyko atidaryti skaitymo failo"

try:
    file_to_write = open(output_filename,"w")
except:
    print "nepavyko atidaryti skaitymo failo"
    
i=0    
for line in fileinput.input(open_filename):
    print "line" + str(i) + "\n"
    print line
    print "\n"
    separated_lines_list = line.split("\t")
    print str(separated_lines_list) + "\n"
    i +=1
    print "length " + str(len(separated_lines_list)) + "\n\n"
    if (i % 15) == 0:
        break

i=0
print "meginsim loopint"
#one line from the text file
for line in fileinput.input(open_filename):
    separated_lines_list = line.split("\t")
    joined_once_again_string = "\t".join(separated_lines_list)
    final_line = joined_once_again_string #+ "\n"
    file_to_write.write(final_line)
    i += 1
    if (i % 1) == 0:
        print str(i) + " exitinu loopea"
        break
#one line from the python code:

separated_inputs = ['1',\
                    'Web comment',\
                    'Delfi',\
                    '2000-05-23 09:36:00',\
                    'Roki\xc5\xa1kio mokytojai pradeda neterminuot\xc4\x85 streik\xc4\x85',\
                    'nicka " sss',\
                    'http://www.delfi.lt/news/daily/lithuania/article.php?id=16015',\
                    'Matyt, kad Paulauskoė kerai stipresni.',\
                    '2009-09-10 17:58:43',\
                    '15',\
                    'defli_14',\
                    ]
one_liner= fields_terminated_by.join(separated_inputs)
final_line =  one_liner + lines_terminated_by
file_to_write.write(final_line)
print "įrašėm eilutę, uždarysim failą"
file_to_write.close()

#for line in input_lines_list:
    #separated_lines_list = line.split("\t")
    #joined_once_again_string = "\t".join(separated_lines_list)
    #final_line = joined_once_again_string + "\n"
    #file_to_write.write(final_line)

skirtums = datetime.datetime.now()-generate_file_start_time

print "pradejom- %s, baigem - %s, uztrukom - %s" % (str(generate_file_start_time),str(datetime.datetime.now()),str(skirtums))
print "============"

#empty table
print "============"
empty_table_start_time = datetime.datetime.now()
print "Emptyinsim lenteles"
truncate_line =\
"""
TRUNCATE
django.documents
"""
session.execute(truncate_line)
skirtums = datetime.datetime.now()-empty_table_start_time
print "pradejom- %s, baigem - %s, uztrukom - %s" % (str(empty_table_start_time),str(datetime.datetime.now()),str(skirtums))
print "============"


#Flush tables
print "============"
flush_table_start_time = datetime.datetime.now()
print "Flushinsim lenteles"
flush_line =\
"""
FLUSH TABLES
"""
session.execute(flush_line)
skirtums = datetime.datetime.now()-flush_table_start_time
print "pradejom- %s, baigem - %s, uztrukom - %s" % (str(flush_table_start_time),str(datetime.datetime.now()),str(skirtums))
print "============"


#Disable indexes
print "============"
disable_indexes_start_time = datetime.datetime.now()
print "disableinsim indexus" #interesting, does index cardinality switches to 0 after this?
subprocess.call("myisamchk --keys-used=0 -rq /home/toinbis/Desktop/programming/369/runtime/mysql_datadir/django/documents",\
                shell=True)
skirtums = datetime.datetime.now()-disable_indexes_start_time
print "pradejom- %s, baigem - %s, uztrukom - %s" % (str(disable_indexes_start_time),str(datetime.datetime.now()),str(skirtums))
print "============"



#Load data infile
print "============"
print "nu tuoj loadinsim duomenis"

load_infile_start_time = datetime.datetime.now()

  
#print load_infile_line
#session.execute(load_infile_line)
#session.commit()

skirtums = datetime.datetime.now()-load_infile_start_time
print "pradejom- %s, baigem - %s, uztrukom - %s" % (str(load_infile_start_time),str(datetime.datetime.now()),str(skirtums))
print "============"


#Recreate indexes
print "============"
print "recreateinsim indexus"
recreate_indexes_start_time = 
subprocess.call("myisamchk -rqa /home/toinbis/Desktop/programming/369/runtime/mysql_datadir/django/documents",\
                shell=True)
skirtums = datetime.datetime.now()-recreate_indexes_start_time
print "pradejom- %s, baigem - %s, uztrukom - %s" % (str(recreate_indexes_start_time),str(datetime.datetime.now()),str(skirtums))
print "============"

print "done"    
"""
TODO:
-find out how to check if the passed unicode string meets the requirements of the given field type of the database.
"""



#smthng like this
#import fileinput
#file_to_write = open("path","w")
#file_to_read = open("path","r")
#i = 0
#for line in fileinput.input(self.input):
    #print line
    #file_to_write.write(line)
    #i +=1
    #if (i % 100000) == 0:
        #print i

        
#try:
    #print str(i) + "eilute" + "\n"
    #print file_to_read.readline(i)
#except:
    #print "atrodo failo galas"
    #sys.exit(2) 

#This way we'd read the short file
#input_file= open(open_filename,'r').read()
#input_lines_list = input_file.split("\n")
#will remove the last element of the list, if it's an empty string
#input_lines_list.remove("")

#s = select([db_table_documents])
#a = db_table_documents.c.contains_column
#rpdb2.start_embedded_debugger("any_password")
#print "labas"
#print a
#print "ba"
#for result in db.execute(s):
#    print result.values()[0]

#print "Hello World"
#rpdb2.start_embedded_debugger("any_password")
#print "Nu jau debuginsim"
#django settings 
#import rpdb2
