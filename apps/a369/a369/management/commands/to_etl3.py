# -*- coding: utf8 -*-
import sys, re, fileinput, os, subprocess, commands, datetime
from django.core.management.base import BaseCommand
from core.models import Documents
from optparse import OptionParser, make_option
import settings
from sqlalchemy import *
from sqlalchemy.orm import *

#import re
#from xml.dom import minidom
#import rpdb2


################
#TODO: 
#  - parametrą normąlų padaryt tarp "-rqa" ir "ALTER TABLE".
#  - pakeist kad dbDest nereiktų source objecto, tik file_path'o 
#  - perdaryti, jog laiką funkcijos kalkuliuotų tik Command().run_txt_export
#    as it's bad to allow functions to calculate their's own run time.
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

-t txtcust, butent sitas parametras paleist customized ETL skripta.


#TODO
-padaryti, kad import'as naudotų ne source objecto file location'ą, o trasnform
global kintamąjį. tegu kas nors ir šitą nustato.

-padaryti, jog line-by-line paparsinus sėkmingai importintų.
-padaryti, jog line-by-line -> to_list -> [mod] -> .join -> list -> line veiktų.


-Sugeneruoja output failiuką iš source_meta lentelės.
-jei perduodama keli mapingai, disable indexes, do both import, enable.

#Done
#notes
The idea is that with txtcust parameter, we use custom 
#Test commands:
$manage to_etl3 -s delficommdb -t txtcust -r 11 -o  
$manage rebuild_index


toinbis@sambook:~/Desktop/programming/369/parts/sphinx/var$ ../bin/indexer --all
toinbis@sambook:~/Desktop/programming/369/parts/sphinx/var$ ../bin/searchd


if txtcust will be used, then in load_txt_from_file 

implement assert(len(splited_lines_list)==



USAGE NOTES:

variables in mappings has to be escaped with \\variable_value\\
"""

########################################################################
root_project_dir_list=\
                     os.path.abspath(os.path.dirname(__file__)).split("/")[:-5]
root_project_dir_string = "/".join(root_project_dir_list)


#global values for counting time
xml_parsing_time = 0
disable_indexes_time = 0
enable_indexes_time = 0
load_into_outfile_txt_or_xml = 0
load_data_infile_txt_or_xml = 0

#global values for parsing
filepathname_of_extaction_file = 0
filepathname_of_parsed_file = 0
filepathname_of_transformed_file = 0

count_successes = 0
count_fails = 0

fields_terminated_by = ":?...::;"
fields_enclosed_by = ""
#this one below doesn't work. to find out why.
fields_escaped_by = ""
lines_terminated_by = ".:.:.:?\n"
lines_starting_by = "...:.:.:"


#So the same command could be used for both import and export!

#custom_params =\
            #"""
            #FIELDS TERMINATED BY '%s' ENCLOSED BY '%s' 
            #LINES TERMINATED BY '%s' STARTING BY '%s'
            #""" %\
                #(fields_terminated_by, fields_enclosed_by, fields_escaped_by,\
                    #lines_terminated_by, lines_starting_by,)

custom_params=\
             """
             FIELDS TERMINATED BY '%s' ENCLOSED BY '%s' ESCAPED BY '%s'
             LINES TERMINATED BY '%s' STARTING BY '%s'
             """ %\
                 (fields_terminated_by, fields_enclosed_by, fields_escaped_by,\
                  lines_terminated_by, lines_starting_by,)

#custom_params = \
                #"""
                #FIELDS TERMINATED BY '%s' 
                #""" %\
                #(fields_terminated_by,)




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

#mapping_defli_to_docs = [{'name':'id', 'var':'','source':None, 'transform':''},\
                         #{'name':'source_type', 'var':'\\article_comment\\',\
                          #'source':None, 'transform':''},\
                         #{'name':'source', 'var':'\\delfi_lt\\', 'source':'', 'transform':''},\
                         #{'name':'date_birth', 'source':'data', 'transform':''},\
                         #{'name':'title', 'source':'Straipsnio_pav', 'transform':''},\
                         #{'name':'nickas', 'source':'nickas', 'transform':''},\
                         #{'name':'linkas', 'source':'Straipsnio_url', 'transform':''},\
                         #{'name':'content', 'source':'turinys', 'transform':''},\
                         #{'name':'ts_insert', 'source':'ts_insert', 'transform':''},\
                         #{'name':'source_id', 'var':"\\101\\", 'source':None, 'transform':''},\
                         #{'name':'surrogate_key', 'var':'\\101'+'defli\\','source':'','transform':''},\
                         #]


mapping_defli_to_docs = [{'name':'id', 'var':'','source':None, 'transform':''},\
                         {'name':'source_type', 'var':'article_comment',\
                          'source':None, 'transform':''},\
                         {'name':'source', 'var':'delfi_lt', 'source':'', 'transform':''},\
                         {'name':'date_birth', 'source':'data', 'transform':''},\
                         {'name':'title', 'source':'Straipsnio_pav', 'transform':''},\
                         {'name':'nickas', 'source':'nickas', 'transform':''},\
                         {'name':'linkas', 'source':'Straipsnio_url', 'transform':''},\
                         {'name':'content', 'source':'turinys', 'transform':''},\
                         {'name':'ts_insert', 'source':'ts_insert', 'transform':''},\
                         {'name':'source_id', 'var':"101", 'source':None, 'transform':''},\
                         {'name':'surrogate_key', 'var':'101'+'defli','source':'','transform':''},\
                         ]

mapping_rsscomments_to_docs = [{'name':'id', 'var':'','source':None, 'transform':''},\
                         {'name':'source_type', 'var':'microblogpost',\
                          'source':None, 'transform':''},\
                         {'name':'source', 'var':'twitter_com', 'source':None, 'transform':''},\
                         {'name':'date_birth', 'source':'date', 'transform':''},\
                         {'name':'title', 'var':'mikrotinklaraščio_irasas', 'source':'', 'transform':''},\
                         {'name':'nickas', 'source':'nickas', 'transform':''},\
                         {'name':'linkas', 'source':'url', 'transform':''},\
                         {'name':'content', 'source':'content', 'transform':''},\
                         {'name':'ts_insert', 'source':'ts_insert', 'transform':''},\
                         {'name':'source_id', 'var':"102", 'source':None, 'transform':''},\
                         {'name':'surrogate_key', 'var':'101'+'twitter','source':'','transform':''},\
                         ]

mapping_list= [mapping_defli_to_docs, mapping_rsscomments_to_docs]

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
class Mapper:
    """
    To be implemented one day.
    That day is not today.
    """

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""

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
        self.create_table_if_it_exists()


    def get_table_list(self):
        """
        TO_BE_IMPLEMENTED
        Prints all the tables of a given database.
        """
        #return self.alchemy_metadata.sorted_tables
        pass

    def get_conn_settings(self):
        """
        Returns the dictionary with db connection parameters.
        The dictionary is crafted by adding table_name key+value to the general
        index of metadata.
        """
        conn_settings_dict = meta_list[self.meta_indx]
        conn_settings_dict["table_name"]= self.table_name
        return conn_settings_dict

    def create_table_if_it_exists(self):
        """
        Checks if the table exists
        """
        try:
            self.alchemy_table = Table(self.table_name, self.alchemy_metadata,\
                                       autoload=True)
            return True
        except:
            return False

    def get_row_count(self):
        """
        TO_BE_IMPLEMENTED
        returns row_count
        """
        #return number_of_rows
        pass

    def get_column_metadata(self):
        """
        TO_BE_IMPLEMENTED
        Returns list of metadata column objects retrieved by SQLAlchemy
        Useful for double-checking that the source->destination  
        """
        pass


########################################################################
class DbSource(DbConn):
    """
    Please, describe who am I
    """

    #----------------------------------------------------------------------
    def __init__(self, tbl_index, tbl_name):
        """Constructor"""
        DbConn.__init__(self, tbl_index, tbl_name)
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


    def dump_data_to_text(self, amount_of_rows=0,custom_separators=False):
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


        if custom_separators:
            print "Well change the bash_command here"        
            bash_command="""%s --user=%s --password=%s -e "
            SELECT *
            INTO OUTFILE '%s' 
            %s
            FROM %s.%s
            %s
            """ %\
                (self.mysql_exec, self.db_user, self.db_pass,\
                 new_filename,\
                 custom_params,\
                 self.db_name, self.table_name,\
                 limit)

        print bash_command
        # 0 is 'success' return code of subprocess.call()
        command_result_msg = subprocess.call(bash_command, shell=True)
        tc.done()
        global load_into_outfile_txt_or_xml
        global filepathname_of_extaction_file
        load_into_outfile_txt_or_xml = tc.total_time
        filepathname_of_extaction_file = new_filename
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
    I commit given sql command on a given DB table.
    """

    #----------------------------------------------------------------------
    def __init__(self, tbl_index, tbl_name, source_object):
        """Constructor"""
        DbConn.__init__(self, tbl_index,tbl_name)
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

    def load_txt_data_infile(self, custom_separators=False):
        #generates such shell command:
        #./bin/mysql  -user=dj --password=djangopass 
        #-D dbname -e "LOAD DATA INFILE 'fname' INTO TABLE db_name.tbl_name"
        tc = TimeCounter("Executing LOAD DATA INFILE")

        #myssql can't write to other but it's data directory, so we switch
        #the output file location here. same done on import part.
        filename = self.source_object.file_data_txt.split("/")[-1:][0]
        new_filename = '/var/lib/mysql/' + filename
        #new_filename = self.source_object.file_data_txt

        bash_command =""" 
        %s  --user=%s --password=%s \
        -e \"LOAD DATA INFILE '%s' INTO TABLE %s.%s" 
        """ %\
            (self.mysql_exec, self.db_user, self.db_pass,\
             new_filename, self.db_name, self.table_name)


        if custom_separators:
            print "We'll change the bash_command here"
            #here the filenamepath we use the global values, set by 
            #instance of ParseMapTransform's instance.
            bash_command =\
                         """ 
            %s  --user=%s --password=%s \
            -e \"LOAD DATA INFILE '%s' INTO TABLE %s.%s \
            %s "
            """ %\
                (self.mysql_exec, self.db_user, self.db_pass,\
                 filepathname_of_transformed_file,\
                 self.db_name, self.table_name,\
                 custom_params)



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



########################################################################
class ParseMapTransform:
    """
    I take input file, transform it, generate output file.
    Input file is an outcome of "SELECT * INTO OUTFILE".
    Output file is an input for "LOAD DATA INFILE" (txt mode only; yet).
    I also need a Mapper() object for guidance on how to map source fields to
    destination fields.
    """
    #----------------------------------------------------------------------
    def __init__(self, inputfilepath, dbsourceinst, modelname, \
                 mapping):
        """Constructor"""
        self.inputfilepath = inputfilepath
        self.outputfilepath = ''
        self.parsedfilepath = ''


        self.timestamp = datetime.datetime.now()

        self.setoutputfilepath_and_global_transform_filepath_and_parse()  
        self.dbsource_inst = dbsourceinst
        self.model_class = modelname
        self.model_instance = self.model_class()
        self.mappdict = mapping
        self.source_column_list = self.get_source_column_list()
        self.dest_column_list = self.get_dest_column_list()
        self.parse_file_remove_endline()
        self.parse_line_by_line_and_write_transformed()
        
        #import rpdb2
        #rpdb2.start_embedded_debugger("labas")

    def get_source_column_list(self):
        source_column = []
        for c in self.dbsource_inst.alchemy_table.columns:
            source_column.append(c.name)
        return source_column

    def get_dest_column_list(self):
        dest_column = []
        listt = self.model_class._meta.fields
        for field in listt:
            dest_column.append(field.name)
        return dest_column


    def setoutputfilepath_and_global_transform_filepath_and_parse(self):
        tmp_project_dir = root_project_dir_list
        dw_dir = "/".join(tmp_project_dir)
        
        global filepathname_of_transformed_file
        filepathname_of_transformed_file = self.outputfilepath\
                                         = "%s%s_data_txt_%s_%s.txt" %\
                                         (dw_dir, "transformed", str(self.timestamp.date()),\
                                          str(self.timestamp.time()))
        
        global filepathname_of_parsed_file
        filepathname_of_parsed_file = "%s%s_data_txt_%s_%sparsed.txt" %\
                                         (dw_dir, "transformed", str(self.timestamp.date()),\
                                          str(self.timestamp.time()))
        
    def parse_line_by_line_and_write_transformed(self):
        try:
            file_to_write = open(filepathname_of_transformed_file,"w")
        except:
            print "nepavyko atidaryti skaitymo failo"
        tc = TimeCounter("Mapping_lists")
        for line in fileinput.input(filepathname_of_parsed_file):
            #rpdb2.start_embedded_debugger("labas")
            if (line[-len(lines_terminated_by):]==lines_terminated_by):
                line = line[:-len(lines_terminated_by)]
            if (line[:len(lines_starting_by)]==lines_starting_by):
                line = line[len(lines_starting_by):]
            separated_lines_list = line.split(fields_terminated_by)
            #separated_lines_list = [elem.strip() for elem in separated_lines_list]
            
            try:
                assert(len(separated_lines_list)==len(self.source_column_list))
            except AssertionError:
                print "asser error"
                print "vim " +str(filepathname_of_extaction_file)
                print "vim " +str(filepathname_of_parsed_file)
                print "vim "+ str(filepathname_of_transformed_file)
                rpdb2.start_embedded_debugger("labas")
                sys.exit(2)
            separated_out_list = self.get_output_list(separated_lines_list)
            self.validate_django_model(separated_out_list)
            one_liner= fields_terminated_by.join(separated_out_list)
            one_liner =  lines_starting_by + one_liner + lines_terminated_by
            file_to_write.write(one_liner+"\n")
        file_to_write.close()
        tc.done()
        
    def parse_file_remove_endline(self):
        tc = TimeCounter("parsing txt file remove ends")
        inputfilepath = filepathname_of_extaction_file
        try:
            file_to_write = open(filepathname_of_parsed_file,"w")
        except:
            print "Failed to open a file remove endline"
            sys.exit(2)

        line_count = 0
        for line in fileinput.input(inputfilepath):
            #print "parsing" + line
            #rpdb2.start_embedded_debugger("labas")
            
            #pabaiga
            if (line[-len(lines_terminated_by):]==lines_terminated_by):
                line_without_termination = line[:-len(lines_terminated_by)]
                separated_lines_list = line_without_termination.split(fields_terminated_by)
                if len(separated_lines_list)==len(self.source_column_list):
                    #print "all fine, case 1"
                    #print line
                    #sys.exit(2)
                    pass
                elif len(separated_lines_list)!=len(self.source_column_list):
                    pass
                    #print "line ending is fine, but not enough columns, case 2"
                else:
                    "how did you got here?"
                    sys.exit(2)
            elif (line[-len(lines_terminated_by):]!=lines_terminated_by):
                if len(separated_lines_list)==len(self.source_column_list):
                    #print "case 3. probably middle of row"
                    #print "line:" + line
                    line=line.rstrip()
                    #print "rstripped line:" + line
                elif len(separated_lines_list)!=len(self.source_column_list):
                    #print "case 4 - nor length, nor end"
                    #print "line:" + line
                    line=line.rstrip()
                    #print "rstripped line:" + line
                else:
                    "how did you got here?"
                    sys.exit(2)
            else:
                "It's impossible to reach this. how you've made it?"
                sys.exit(2)
            
            #to avoid "delficommdb 72" effect
            if line!="\n":        
                file_to_write.write(line)
            #line_count += 1
            #if line_count%1 == 0:
            #    tc.checkpoint("parsing %i rows" % (line_count,))
        file_to_write.close()
        print "closed file"
        tc.done()
        pass


  
    

    def remove_whitespace(self,line):
        return removed_whitespace_line

    #helper function, to get 
    def get_class(self, kls):
        parts = kls.split('.')
        module = ".".join(parts[:-1])
        m = __import__( module )
        for comp in parts[1:]:
            m = getattr(m, comp)            
        return m

    def get_output_list(self, line_list):
        input_cols = self.source_column_list
        output_cols = self.dest_column_list
        #import rpdb2
        #rpdb2.start_embedded_debugger("labas")
        #check if the length if columns equals lenght of values
        #print len(line_list)
        #print len(input_cols)
        try:
            assert(len(input_cols)==len(line_list))
        except AssertionError:
            #rpdb2.start_embedded_debugger("labas")
            print "Inside mapping"
            sys.exit(2)

        output_list=[]
        #rpdb2.start_embedded_debugger("labas")
        for i in range(len(output_cols)):
            output_list.append('')
            map_dict = self.mappdict[i]
            if 'var' in map_dict:
                output_list[i]=str(map_dict["var"])
            elif map_dict["source"] != None:
                source_col_name=map_dict['source']
                source_col_index = input_cols.index(source_col_name)
                output_list[i]=str(line_list[source_col_index])
            else:
                output_list[i]=""
        return output_list

    def validate_django_model(self, value_list):
        try:
            assert(len(value_list)==len(self.dest_column_list))
        except:
            print "inide validation"
            sys.exit(2)
        mod_instance = self.model_instance
        #rpdb2.start_embedded_debugger
        for i in range(len(self.dest_column_list)):
            setattr(mod_instance, self.dest_column_list[i], value_list[i])
        try:
            mod_instance.full_clean()
        except:
            print "invalid model"
            #rpdb2.start_embedded_debugger("labas")
            sys.exit(2)


class Command(BaseCommand):
    """
    A class Command in a custom-command's module is a must (Django requirement).
    Option's list below is for source db, as the destination setting's
    are imported directly from django's settings.py.
    """
    option_list = BaseCommand.option_list + (
        make_option("-o", "--source_meta", dest="source_metadata",\
                    default=1),
        make_option("-d", "--destination_meta", dest="destination_metadata",\
                    default=0),
        make_option("-s", "--source_table", dest="source_table",\
                    default="delficommdb"),
        make_option("-m", "--mapping", dest="mapping",\
                    default=0),
        make_option("-r", "--row_count", dest="row_count",\
                    default=0),
        make_option("-t", "--type", dest="type",\
                    default="txt"),
        make_option("-p", "--parse", dest="parse",\
                    default=0),
    )



    def run_xml_export(self,sourcee, amount_of_rows=0,parse=0):
        #sourcee.dump_table_metadata_to_xml()

        sourcee.output_createtable_sql_syntax_to_file()
        sourcee.dump_table_data_to_xml(amount_of_rows)
        if parse==0:
            pass
        elif parse==1:
            sourcee.parse_xml()
        else: 
            print "-p --parse can only have values [0|1]"

    def run_xml_import(self,dbdest,parse=0):
        dbdest.create_table_from_sql()
        dbdest.disable_indixes(1)
        dbdest.load_xml_data_infile(parse)
        dbdest.enable_indixes(1)


    def run_txt_export(self, sourcee, amount_of_rows=0, custom_sep=False):
        #sourcee.dump_table_metadata_to_xml()
        #not used for custtxt. make it depend on a custom_sep conditional value.
        sourcee.output_createtable_sql_syntax_to_file()
        sourcee.dump_data_to_text(amount_of_rows, custom_sep)

    def run_txt_import(self, dbdest, custom_sep=False):
        dbdest.create_table_from_sql()
        dbdest.disable_indixes()
        dbdest.load_txt_data_infile(custom_sep)
        dbdest.enable_indixes()

    def transformmap(self, filepath, dbsource_instance, model_class, mappdict):
        transform_instance = ParseMapTransform(filepath ,dbsource_instance, model_class, mappdict)

    def handle(self, *args, **options):
        """
        A must-be-inplemented method (Django req.), which is launched fist.
        """
        #HACK, type parsing
        options["parse"] = int(options["parse"])
        options["destination_metadata"] = int(options["destination_metadata"])
        options["source_metadata"] = int(options["source_metadata"])
        options["mapping"] = int(options["mapping"])
        
        #here the source object is created
        sourcee = DbSource(options["source_metadata"],\
                           options["source_table"],\
                           )

        #Start script
        tc1=TimeCounter("ETL script")
        print "tc1" + str(tc1.starttime)

        #Export part############################################
        tc2=TimeCounter("Extract part")
        print "tc2" + str(tc2.starttime)

        #Default case
        if options["type"]=="txt":
            self.run_txt_export(sourcee,options["row_count"])
        elif options["type"]=="txtcust":
            ##############
            ##this is the function for real ETL
            ##############
            #print "that will be an extract part"
            self.run_txt_export(sourcee,options["row_count"],\
                                custom_sep=True)
            print "exportinom i %s" % (filepathname_of_extaction_file,)
            ###############
        elif options["type"]=="xml":
            self.run_xml_export(sourcee,options["row_count"], options["parse"])
        else:
            print "'xml' and 'txt' ar the only available type options"

        tc2.done()


        #Transform part#############################################
        tc4=TimeCounter("Transform part")
        if options["type"]=="txt":
            print "For txt we don't transform anything" 
        elif options["type"]=="txtcust":
            #rpdb2.start_embedded_debugger("labas")
            self.transformmap(filepathname_of_extaction_file, sourcee,
                              Documents, mapping_list[options['mapping']])

            #print "here will be transformation part"
        elif options["type"]=="xml":
            print "For txt we don't do anything"
        else:
            print "'xml' and 'txt' and 'txtcust' ar the only available type options"
        tc4.done()
        #Import part#################################	###############
        tc3 = TimeCounter("Import part")
        dbdest = DbDest(options["destination_metadata"],\
                        "documents", sourcee)

        if options["type"]=="txt":
            self.run_txt_import(dbdest)  
        elif options["type"]=="txtcust":
            ##############
            #pass
            #print "that will be a load part" 
            self.run_txt_import(dbdest,custom_sep=True,)
        elif options["type"]=="xml":
            self.run_xml_import(dbdest,options["parse"])
        else:
            print "'xml' and 'txt' and 'txtcust' ar the only type options"

        tc3.done()
        #Done Import###########################################################
        tc1.done()
        print "vim " +str(filepathname_of_extaction_file)
        print "vim " +str(filepathname_of_parsed_file)
        print "vim "+ str(filepathname_of_transformed_file)
        print "diff %s %s" % (filepathname_of_extaction_file,\
                              filepathname_of_parsed_file)
        print str(count_successes) + " success lines"
        print str(count_fails) + " fail lines"
        #Done All work, only reporting left