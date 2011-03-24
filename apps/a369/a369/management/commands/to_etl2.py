# -*- coding: utf8 -*-
import sys, re, fileinput, os, subprocess, commands, datetime
from django.core.management.base import BaseCommand
from core.models import Documents
from optparse import OptionParser, make_option
import settings
from sqlalchemy import *
from sqlalchemy.orm import *
#import wingdbstub
#import re
#from xml.dom import minidom
#import rpdb2


################
#TODO: 
#  -parametrą normąlų padaryt tarp "-rqa" ir "ALTER TABLE".
#  -pakeist kad dbDest nereiktų source objecto, tik file_path'o 
################

"""
The point of this module:
Sugeneruoja output failiuką iš source_meta lentelės.

Jį transformuoja į input failiuką.

Input failiuką suimportuoja į dest_meta.

For instance:
$manage to_etl -source meta_dict -destdb meta_dict -mapper mapper_name -type [xml|txt]

meta_dict_example = {
    'metadata_desc':'buildout mysql, Default Django DB',\
    'db_engine': settings.DATABASE_ENGINE,\
    'db_name' : settings.DATABASE_NAME,\
    'db_pass' : settings.DATABASE_PASSWORD,\
    'db_port' : settings.DATABASE_PORT,\
    'db_user' : settings.DATABASE_USER,\
    'db_socket' : settings.DATABASE_HOST,\
    'mysqldump_executable' : "%s/parts/mysql/bin/mysqldump"%
    (root_project_dir_string,),
    'mysql_executable' : "%s/bin/mysql"%\
    (root_project_dir_string,),
    'myisamchk_executable' : "%s/parts/mysql/bin/myisamchk"%\
    (root_project_dir_string,),
    'mysql_datadir' : "%s/runtime/mysql_datadir"%\
    (root_project_dir_string,),
}

mapper class:

turi tuple dict'ų:

({'source_':'dest_table', },


#TODO
- 

#Done

"""
 
 
 


########################################################################
root_project_dir_list=\
                     os.path.abspath(os.path.dirname(__file__)).split("/")[:-5]
root_project_dir_string = "/".join(root_project_dir_list)

xml_parsing_time = 0
disable_indexes_time = 0
enable_indexes_time = 0
load_into_outfile_txt_or_xml = 0
load_data_infile_txt_or_xml = 0


########################################################################
#List of DB/Table connection settings

meta_0 = {
    'metadata_desc':'buildout mysql, Default Django DB',\
    'db_engine': settings.DATABASE_ENGINE,\
    'db_name' : settings.DATABASE_NAME,\
    'db_pass' : settings.DATABASE_PASSWORD,\
    'db_port' : settings.DATABASE_PORT,\
    'db_user' : settings.DATABASE_USER,\
    'db_socket' : settings.DATABASE_HOST,\
    'mysqldump_executable' : "%s/parts/mysql/bin/mysqldump"%
    (root_project_dir_string,),
    'mysql_executable' : "%s/bin/mysql"%\
    (root_project_dir_string,),
    'myisamchk_executable' : "%s/parts/mysql/bin/myisamchk"%\
    (root_project_dir_string,),
    'mysql_datadir' : "%s/runtime/mysql_datadir"%\
    (root_project_dir_string,),
}

meta_1 = {
    'metadata_desc':'ubuntu mysql, DB alchemy',\
    'db_engine': "mysql",\
    'db_name' : "alchemy",\
    'db_pass' : "djangopass",\
    'db_port' : "3306",\
    'db_user' : "django",\
    'db_socket' : "/var/run/mysqld/mysqld.sock",\
    'mysqldump_executable' :'mysqldump',\
    'mysql_executable' : 'mysql',\
    'myisamchk_executable' : 'myisamchk',\
    'mysql_datadir' : '/var/lib/mysql',\
}

#meta settings' container
meta_list = [meta_0,meta_1]


map_0 = {

}

map_1 = {

}

map_list = [map_0,map_1]


########################################################################
class TimeCounter:
    """
    Tracks time it takes to process the method call, generates pretty output.
    Useful when debuging/optimizing import of 15+ GB XML file:) 
    """
    
    #----------------------------------------------------------------------
    def __init__(self, msg):
        """Constructor"""
        self.stat_msg = msg
        self.starttime = datetime.datetime.now()
        self.last_checkpoint = datetime.datetime.now()
        print "===================================="
        print "Starting %s" %(msg,) 
    
    def checkpoint(self, msg):
        print "-------------------------------------"
        print '%s took %s' % (msg,\
                            datetime.datetime.now()-self.last_checkpoint)
        print "-------------------------------------"
        self.last_checkpoint = datetime.datetime.now()
        
    def done(self):
        self.finishtime = datetime.datetime.now()
        self.total_time = self.finishtime - self.starttime
        print "\nfinished %s in %s " %\
        (self.stat_msg, self.total_time)
        print "=====================================\n"

########################################################################
class Mapper(object):
    """
    To be implemented one day.
    That day is not today.
    """

    #----------------------------------------------------------------------
    def __init__(self, src_oject, dst_object, map_index, fltype, trans_type):
        """Constructor"""
        #if not dst_object.check_if_table_exists():
        pass
            
        
        

########################################################################
class DbConn(object):
    """
    Connection's metadata Class. which itself describes (mysql's) db table's
    properties that are necessary to perform "mysqldump --xml"
    and "LOAD XML INFILE" ETL procedures.    
    """
    #----------------------------------------------------------------------
    def __init__(self, meta_index, table_name):
        """Constructor"""  
        self.timestamp = datetime.datetime.now()

        self.db_engine = meta_list[meta_index]['db_engine']
        self.db_name = meta_list[meta_index]['db_name']
        self.db_pass = meta_list[meta_index]['db_pass']
        self.db_port = meta_list[meta_index]['db_port']
        self.db_user = meta_list[meta_index]['db_user']
        self.db_socket = meta_list[meta_index]['db_socket']
        self.mysqldump_exec = meta_list[meta_index]['mysqldump_executable']
        self.mysql_exec = meta_list[meta_index]['mysql_executable']
        self.myisamchk_exec = meta_list[meta_index]['myisamchk_executable']
        self.mysql_datadir = meta_list[meta_index]['mysql_datadir']
        self.table_name = table_name
        self.meta_indx = meta_index
        self.db_conn_row =\
         "%s://%s:%s@localhost:%s/%s?use_unicode=1&charset=utf8&unix_socket=%s"\
            % (self.db_engine,self.db_user,self.db_pass,\
               self.db_port, self.db_name, self.db_socket)
        self.alchemy_engine = create_engine(self.db_conn_row)
        self.alchemy_metadata = MetaData()
        self.alchemy_metadata.bind = self.alchemy_engine
        self.Session = sessionmaker(bind=self.alchemy_engine)
        self.session = self.Session()
        #if the table exists, let's make a list of it's columns as an attribute
        if self.check_if_table_exists():
            self.set_column_list()
            
    def get_conn_settings(self):
        """
        Returns the dictionary with db connection parameters.
        The dictionary is crafted by adding table_name key+value to the general
        index of metadata.
        """
        conn_settings_dict = meta_list[self.meta_indx]
        conn_settings_dict["table_name"]= self.table_name
        return conn_settings_dict

    def check_if_table_exists(self):
        """
        Checks if the table exists
        """
        try:
            self.alchemy_table = Table(self.table_name, self.alchemy_metadata,\
                                       autoload=True)
            return True
        except:
            return False
        
    def set_column_list(self):
        self.alchemy_column_metadata_list = []
        for c in self.alchemy_table.columns:
            self.alchemy_column_metadata_list.append(c)
        
           
    #def get_row_count(self):
        #"""
        #TO_BE_IMPLEMENTED
        #returns row_count
        #"""
        
        ##return number_of_rows
        #pass
     #def get_table_list(self):
        #"""
        #TO_BE_IMPLEMENTED
        #Prints all the tables of a given database.
        #"""
        ##return self.alchemy_metadata.sorted_tables
        #pass


########################################################################
class DbSource(DbConn):
    """
    Please, describe who am I
    """

    #----------------------------------------------------------------------
    def __init__(self, db_metadata_index, tbl_name):
        """Constructor"""
        DbConn.__init__(self, db_metadata_index, tbl_name)
        tmp_project_dir = root_project_dir_list
        tmp_project_dir.append('dw')
        tmp_project_dir.append('')
        dw_dir = "/".join(tmp_project_dir)
        
        self.file_meta_sql = "%s%s_meta_sql_%s_%s.sql" %\
        (dw_dir, self.table_name, str(self.timestamp.date()),\
         str(self.timestamp.time()))
    
        self.file_meta_xml = "%s%s_meta_xml_%s_%s.xml" %\
        (dw_dir, self.table_name, str(self.timestamp.date()),\
         str(self.timestamp.time()))
        
        self.file_data_txt = "%s%s_data_txt_%s_%s.txt" %\
        (dw_dir, self.table_name, str(self.timestamp.date()),\
         str(self.timestamp.time())) 
        
        self.file_data_xml = "%s%s_data_xml_%s_%s.xml" %\
        (dw_dir, self.table_name, str(self.timestamp.date()),\
         str(self.timestamp.time())) 

    def output_createtable_sql_syntax_to_file(self):
        #generates such shell command:
        #mysqldump --user=django --password=djangopass -d db_name db_pass
        tc = TimeCounter("outputing CREATE TABLE sql syntax to file")
        bash_command = "%s --user=%s --password=%s -d %s %s > %s" %\
                     (self.mysqldump_exec, self.db_user, self.db_pass,\
                      self.db_name, self.table_name, self.file_meta_sql)
        
        # 0 is 'success' return code of subprocess.call()
        print bash_command
        command_result_msg = subprocess.call(bash_command, shell=True)
        tc.done()
        return command_result_msg

    def dump_table_metadata_to_xml(self):
        """
        Generates & executes such shell command:
        mysqldump --user=django --password=djangopass --xml -d db_name db_pass
        returns False(0) on success, >0 in a failure
        """
        bash_command = "%s --user=%s --password=%s --xml -d %s %s > %s" %\
                     (self.mysqldump_exec, self.db_user, self.db_pass,\
                      self.db_name, self.table_name, self.file_meta_xml)
        
        # 0 is 'success' return code of subprocess.call()
        return subprocess.call(bash_command, shell=True)
    
    
    def dump_data_to_text(self, amount_of_rows=0):
        #generates such shell command:
        #./bin/mysql  -user=dj --password=djangopass 
        # -e "SELECT * INTO OUTFILE 'fname' FROM TABLE db_name.tbl_name"
        tc = TimeCounter("SELECT * INTO OUTFILE")
        
        #myssql can't write to other but it's data directory, so we switch
        #the output file location here. same done on export part.
        filename = self.file_data_txt.split("/")[-1:][0]
        new_filename = self.mysql_datadir + '/' + filename
        
        if amount_of_rows:
            limit = "LIMIT %s \"" % (amount_of_rows,)
        else:
            limit = "\""
        
        bash_command="""%s --user=%s --password=%s -e "
        SELECT *
        INTO OUTFILE '%s'
        FROM %s.%s
        %s
        """ %\
                     (self.mysql_exec, self.db_user, self.db_pass,\
                      new_filename, self.db_name, self.table_name,\
                      limit)
        
       #bash_command =\
    #"%s --user=%s --password=%s -e \"SELECT * INTO OUTFILE '%s' FROM %s.%s\"" %\
                     #(self.mysql_exec, self.db_user, self.db_pass,\
                      #new_filename,\
                      #self.db_name, self.table_name)
 
        print bash_command
        # 0 is 'success' return code of subprocess.call()
        command_result_msg = subprocess.call(bash_command, shell=True)
        tc.done()
        global load_into_outfile_txt_or_xml
        load_into_outfile_txt_or_xml = tc.total_time
        return command_result_msg
        

    def dump_table_data_to_xml(self, amount_of_rows=0):
        """
        MySQLdump command to output data to xml. 
        SELECT * INTO OUTFILE is impossible due to it doesn't support xml 
        output.
        """
        tc = TimeCounter("outputing table data to xml file")
        print "ammount ="  + str(amount_of_rows)
        if amount_of_rows:
            limit = "--where=\"true LIMIT %s \" " % (amount_of_rows,)
            print "limit= " + str(limit)
        else:
            limit = ""
            print "limit= " + str(limit)
            
        #generates shell command:
        #mysqldump --user=username --password=password  --xml db_name db_pass
        bash_command = "%s --user=%s --password=%s %s --xml %s %s > %s" %\
                     (self.mysqldump_exec, self.db_user, self.db_pass,\
                      limit, self.db_name, self.table_name,\
                      self.file_data_xml)
        print bash_command        
        # 0 is 'success' return code of subprocess.call()
        command_result_msg = subprocess.call(bash_command, shell=True)
        tc.done()
        global load_into_outfile_txt_or_xml
        load_into_outfile_txt_or_xml = tc.total_time
        return command_result_msg
    
    def parse_xml(self):
        """
        Parses xml output and swaps <field name="commets_feed" xsi:nil="true" />
        with <field name="commets_feed">''</field> Or ><field>
        TODO: implement line changes with xml/xslt and with regexp and check
        the speed difference.
        
        Writes output to dataxml.fixed
        """
        tc = TimeCounter("parsing xml file")

        file_to_write = self.file_data_xml + "fixed"
        try:
            file_to_write = open(file_to_write,"w")
        except:
            print "Failed to open a file"
            sys.exit(2)
            
        line_count = 0
        for line in fileinput.input(self.file_data_xml):
            if (line.find('xsi:nil')>0):
                new_line =\
                 line.replace(" xsi:nil=\"true\" />", "></field>")
                file_to_write.write(new_line)
            else:
                file_to_write.write(line)
            line_count += 1
            if line_count%1000 == 0:
                tc.checkpoint("parsing %i rows" % (line_count,))
        file_to_write.close()
        print "closed file"
        
        tc.done()
        global xml_parsing_time
        xml_parsing_time = tc.total_time
         
        
        
########################################################################
class DbDest(DbConn):
    """
    Please, describe who am I
    """

    #----------------------------------------------------------------------
    def __init__(self, db_metadata_index, tbl_name, source_object):
        """Constructor"""
        DbConn.__init__(self, db_metadata_index, tbl_name)
        self.source_object = source_object

    def create_table_from_sql(self):
        #generates such shell command:
        #./bin/mysql  -user=dj --password=djangopass -D dbname -e "source fname"
        bash_command = "%s --user=%s --password=%s -D %s -e 'source %s'" %\
                     (self.mysql_exec, self.db_user, self.db_pass,\
                      self.db_name, self.source_object.file_meta_sql)
        # 0 is 'success' return code of subprocess.call()
        return subprocess.call(bash_command, shell=True)

    def crate_table_from_xml(self):
        """
        To implement one day, at least for simple scenarios.
        """
        pass

    def load_xml_data_infile(self,parse=0):
        #http://dev.mysql.com/doc/refman/5.5/en/load-xml.html
        #generates such shell command:
        #./bin/mysql  -user=dj --password=djangopass 
        #-D dbname -e "LOAD XML INFILE 'fname' INTO TABLE db_name.tbl_name"
        tc = TimeCounter("Executing LOAD XML INFILE")
        
        
        filename = self.source_object.file_data_xml+"fixed"
        
        print "parse ="  + str(parse)
        if parse==0:
            filename = self.source_object.file_data_xml
        else:
            filename = self.source_object.file_data_xml+"fixed"
        
        bash_command =\
    "%s --user=%s --password=%s -e \"LOAD XML INFILE '%s' INTO TABLE %s.%s\"" %\
                     (self.mysql_exec, self.db_user, self.db_pass,filename,\
                      self.db_name, self.table_name)
        
        print bash_command
        # 0 is 'success' return code of subprocess.call()
        command_result_msg = subprocess.call(bash_command, shell=True)
        tc.done()
        global load_data_infile_txt_or_xml
        load_data_infile_txt_or_xml = tc.total_time
        return command_result_msg
    
    def load_txt_data_infile(self):
        #generates such shell command:
        #./bin/mysql  -user=dj --password=djangopass 
        #-D dbname -e "LOAD DATA INFILE 'fname' INTO TABLE db_name.tbl_name"
        tc = TimeCounter("Executing LOAD DATA INFILE")
        
        #myssql can't write to other but it's data directory, so we switch
        #the output file location here. same done on import part.
        filename = self.source_object.file_data_txt.split("/")[-1:][0]
        new_filename = '/var/lib/mysql/' + filename
        #new_filename = self.source_object.file_data_txt
        
        bash_command =\
    "%s --user=%s --password=%s -e \"LOAD DATA INFILE '%s' INTO TABLE %s.%s\"" %\
                     (self.mysql_exec, self.db_user, self.db_pass,\
                      new_filename, self.db_name, self.table_name)

        print bash_command
        # 0 is 'success' return code of subprocess.call()
        command_result_msg = subprocess.call(bash_command, shell=True)
        tc.done()
        
        global load_data_infile_txt_or_xml
        load_data_infile_txt_or_xml = tc.total_time
        return command_result_msg
    
    def disable_indixes(self, via_sqlalchemy=0):
        tc = TimeCounter("Disabling MyISAM indexes")
        
        if via_sqlalchemy==0:    
            bash_command = "%s --keys-used=0 -rq %s/%s/%s" %\
                         (self.myisamchk_exec, self.mysql_datadir,\
                          self.db_name, self.table_name,)
            print bash_command
            command_result_msg = subprocess.call(bash_command, shell=True)
        elif via_sqlalchemy==1:
            print "disabling indexes via sqlalchemy"
            sql_line="ALTER TABLE %s ENABLE KEYS" % (self.table_name,)
            self.session.execute(sql_line)
            self.session.commit()
        else:
            print "wrong value of via_sqlalchemy, only [0|1] supported"
            sys.exit(2)

        tc.done()
        global disable_indexes_time
        disable_indexes_time = tc.total_time
        #return command_result_msg
    
    def enable_indixes(self, via_sqlalchemy=0):
        tc = TimeCounter("Recreating MyISAM indexes")
        
        if via_sqlalchemy==0:
            print "reenabling indexes via bash"
            bash_command = "%s -rqa %s/%s/%s" %\
                         (self.myisamchk_exec, self.mysql_datadir,\
                          self.db_name, self.table_name,)
            print bash_command
            command_result_msg = subprocess.call(bash_command, shell=True)
        elif via_sqlalchemy==1:
            print "reenabling indexes via sqlalchemy"
            sql_line="ALTER TABLE %s ENABLE KEYS" % (self.table_name,)
            self.session.execute(sql_line)
            self.session.commit()
        else:
            print "wrong value of via_sqlalchemy, only [0|1] supported"
            sys.exit(2)
        tc.done()
        global enable_indexes_time
        enable_indexes_time = tc.total_time
        #return command_result_msg

class Command(BaseCommand):
    """
    A class Command in a custom-command's module is a must (Django requirement).
    Option's list below is for source db, as the destination setting's
    are imported directly from django's settings.py.
    """
    option_list = BaseCommand.option_list + (
        make_option("-s", "--source_db", dest="source_db_index",\
                    default=1),
        make_option("-d", "--destination_db", dest="destination_db_index",\
                    default=0),
        make_option("-a", "--source_table", dest="source_table",\
                    default="delficommdb"),
        make_option("-e", "--destination_table", dest="destination_table",\
                    default=Documents._meta.db_table),
        make_option("-r", "--row_count", dest="row_count",\
                    default=0),
        make_option("-t", "--type", dest="type",\
                    default="txt"),\
        make_option("-n", "--transformation_type", dest="transformation_type",\
                    default="parse"), #(parse|SQL)
        make_option("-m", "--mapping_index", dest="mapping_index",\
                    default="0"),
        #make_option("-p", "--parse", dest="parse",\
                    #default=0),
    )
    

            
    
    def handle(self, *args, **options):
        """
        A must-be-inplemented method (Django req.), which is launched fist.
        """
        #options["parse"] = int(options["parse"])
       
        #Management part
        print "I start handle script"
        
        source_object = DbSource(options["source_db_index"],\
                           options["source_table"],)
        
        destination_object = DbDest(options["destination_db_index"],\
                           options["destination_table"],\
                           source_object,)
        
        mapper_object = Mapper(source_object,destination_object,\
                               options["mapping_index"],\
                               options["type"],\
                               options["transformation_type"]
                               )
        
        print "test"
        #import rpdb2
        #rpdb2.start_embedded_debugger("pass")
        
        
        print "labas"
        
        #print "parse value= " +str(options["parse"])\
        #      + "  " + str(type(options["parse"]))
        #sourcee = DbSource(options["source_metadata"],\
        #                   options["source_table"],\
        #                   )
        
        
        
        ##Start script
        #tc1=TimeCounter("ETL script")
        #print "tc1" + str(tc1.starttime)
        
        ##Export part
        #tc2=TimeCounter("Export part")
        #print "tc2" + str(tc2.starttime)
        
        
        
        #====
        #initial part
        #====
            

    #def run_xml_export(self,sourcee, amount_of_rows=0,parse=0):
        ##sourcee.dump_table_metadata_to_xml()

        #sourcee.output_createtable_sql_syntax_to_file()
        #sourcee.dump_table_data_to_xml(amount_of_rows)
        #if parse==0:
            #pass
        #elif parse==1:
            #sourcee.parse_xml()
        #else: 
            #print "-p --parse can only have values [0|1]"
        
    #def run_xml_import(self,dbdest,parse=0):
        #dbdest.create_table_from_sql()
        #dbdest.disable_indixes()
        #dbdest.load_xml_data_infile(parse)
        #dbdest.enable_indixes()

        
    #def run_txt_export(self, sourcee, amount_of_rows=0):
        ##sourcee.dump_table_metadata_to_xml()
        #sourcee.output_createtable_sql_syntax_to_file()
        #sourcee.dump_data_to_text(amount_of_rows)
        
    #def run_txt_import(self, dbdest):
        #dbdest.create_table_from_sql()
        #dbdest.disable_indixes()
        #dbdest.load_txt_data_infile()
        #dbdest.enable_indixes()
        
        #===
        #handle method
        #====
        
        #if options["type"]=="txt":
                    #self.run_txt_export(sourcee,options["row_count"])
        #elif options["type"]=="xml":
            #self.run_xml_export(sourcee,options["row_count"], options["parse"])
        #else:
            #print "'xml' and 'txt' ar the only available type options"
        
        #tc2.done()
        
        ##Import part
        #tc3 = TimeCounter("Import part")
        #dbdest = DbDest(options["destination_metadata"],\
                           #sourcee.table_name, sourcee\
                           #)
        
        #if options["type"]=="txt":
            #self.run_txt_import(dbdest)  
        #elif options["type"]=="xml":
            #self.run_xml_import(dbdest,options["parse"])
        #else:
            #print "'xml' and 'txt' ar the only available type options"
        
        #tc3.done()        
        ##Finish script
        #tc1.done()
        #######################################
        
        
        #print "SELECT * INTO OUTFILE tool %s" %\
            #(str(load_into_outfile_txt_or_xml))
        #print "LOAD DATA INFILE took %s" %\
            #(str(load_data_infile_txt_or_xml))
        #print "ReEnable indexes part took %s" %\
            #(str(enable_indexes_time))
        #print "Whole script took %s" %\
             #(str(tc1.total_time))
        
            #print "Export part took %s" %\
            #     (str(tc2.total_time))
            #print "Disable indexes part took %s" %\
            #     (str(disable_indexes_time))
            #time_overall = tc2.total_time+tc3.total_time
            #if (time_overall<=tc1.total_time):
                #print "gerai; skirtumas" + str(tc1.total_time-time_overall)
            #else:
                #print "blogai; skirtumas" + str(tc1.total_time-time_overall)
        
        #if options["type"]=="xml":
            #if options["parse"]==0:
                #print "Export part took %s" %\
                 #(str(tc2.total_time))
            #elif options["parse"]==1:
                #print "Export part without xml parsing took:%s-%s=%s" %\
                 #(str(tc2.total_time), str(xml_parsing_time),\
                     #str(tc2.total_time-xml_parsing_time))
            #else:
                #print "wrong parse value"
                #sys.exit(2)
            #print "Disable indexes part took %s" %\
                 #(str(disable_indexes_time))
            #print "Import part took %s" %\
                  #(str(tc3.total_time))
            #print "ReEnable indexes part took %s" %\
                 #(str(enable_indexes_time))
            #if options["parse"]==0:
                #print "Whole script took %s" %\
                  #(str(tc1.total_time))
            #else:
                #print "Whole ETL script without xml parsing took: %s-%s=%s" %\
                  #(str(tc1.total_time), str(xml_parsing_time),\
                      #str(tc1.total_time-xml_parsing_time)