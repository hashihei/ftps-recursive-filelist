#
# Copyright <2020> <hashihei>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

#
# Import library
#
import ftplib
import ssl
import datetime
import sys
import logging
import traceback

#
# define for FTP Class
#
class ManuplateFTP():
    ftp_session = None
    _org_makeport = None
    port = 0
    host = ""

    def __init__(self):
        #define class logger
        self.logger = logging.getLogger('ManuplateFTP.Class')
        self.ftp_session = None
        self._org_makeport = None


    def Output_Error(self,Function_Name,e):
        try:
            self.logger.info('%s %s %s %s', datetime.datetime.now(), Function_Name, sys._getframe().f_code.co_name, e.args)
            return 0
        except Exception as e:
            self.logger.info('%s %s %s', datetime.datetime.now(), sys._getframe().f_code.co_name, e.args)
            self.logger.info('%s', traceback.print_exc())
            return -1 

    def Output_Error_onlyMSG(self,Function_Name,msg):
        try:
            self.logger.info('%s %s %s %s', datetime.datetime.now(), Function_Name, sys._getframe().f_code.co_name, msg)
            return 0
        except Exception as e:
            #Other error.
            self.logger.info('%s %s %s', datetime.datetime.now(), sys._getframe().f_code.co_name, e.args)
            self.logger.info('%s', traceback.print_exc())
            return -1 


    def Create_SessionFTPS(self, host, account, password,Mode_PASV="true",PORT=21):

        try:
            #save host,port
            self.port = PORT
            self.host = host

            #create context use TLS v1.2
            ctx = ssl._create_stdlib_context(ssl.PROTOCOL_TLSv1_2)    
            
            #open connection.
            self.ftp_session = ftplib.FTP_TLS(host,context=ctx)

            #for debug
            #self.ftp_session.set_debuglevel(2)

            #Login
            self.ftp_session.login(account,password)
            #ftp mode.
            self.ftp_session.set_pasv(Mode_PASV)
            #secure data connection.
            self.ftp_session.prot_p()
            
            return 0
        except ftplib.error_reply as e:
            #unexpected response.
            self.Output_Error(sys._getframe().f_code.co_name, e)
            return -1
        except ftplib.error_temp as e:
            #temporary error.(code 400--499)
            self.Output_Error(sys._getframe().f_code.co_name, e)
            return -1
        except ftplib.error_perm as e:
            #permanent error.(code 500--599)
            self.Output_Error(sys._getframe().f_code.co_name, e)
            return -1
        except ftplib.error_proto as e:
            #Unknown response code.
            self.Output_Error(sys._getframe().f_code.co_name, e)
            return -1
        except Exception as e:
            #Other error.
            self.Output_Error(sys._getframe().f_code.co_name, e)
            return -1

    def ftp_cwd(self,path):
        try:
            self.ftp_session.cwd(path)
            return 0
        except Exception as e:
            #Other error.
            self.Output_Error(sys._getframe().f_code.co_name, e)
            return -1           

    def ftp_quit(self):
        try:
            self.ftp_session.quit()
            self.ftp_session = None
            return 0
        except Exception as e:
            #Other error.
            self.Output_Error(sys._getframe().f_code.co_name, e)
            return -1       

    def ftp_nlst(self,FILTER=""):
        try:
            nlst = self.ftp_session.nlst(FILTER)
            return nlst
        except Exception as e:
            #Other error.
            self.Output_Error(sys._getframe().f_code.co_name, e)
            return None               

    def ftp_delete(self,FileName):
        try:
            return_code = self.ftp_session.delete(FileName)
            if '250' in return_code:
                #FTP DELE command successful.
                return 0
            else:
                #error.
                self.Output_Error_onlyMSG(sys._getframe().f_code.co_name, return_code)
                return -1
        except Exception as e:
            #Other error.
            self.Output_Error(sys._getframe().f_code.co_name, e)
            return -1  

    def ftp_put(self,Local_File_Name,Remote_File_Name=''):

        try:
            if Remote_File_Name == '' :
                Remote_File_Name = Local_File_Name
            self.ftp_session.storbinary("STOR " + Remote_File_Name, open(Local_File_Name, "rb"))
            return 0
        except IOError as e:
            self.Output_Error(sys._getframe().f_code.co_name, e)
            return -1
        except Exception as e:
            #Other error.
            self.Output_Error(sys._getframe().f_code.co_name, e)
            return -1  
