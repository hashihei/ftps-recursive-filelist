#
# Copyright <2023> <hashihei>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

#
# import
#
import datetime
import sys
import os
from pathlib import Path
import logging
import traceback
import argparse

# import orig Class and Functions
from src.manuplate_ftp import ManuplateFTP
from src import myftps

#
# logging setting.
#
LOGGING_FILE = ""


#WorkDir
WORKDIR = str(Path.cwd())
FOLDER_SIG = os.path.sep

#
# Add command arg.
#
parser = argparse.ArgumentParser()
parser.add_argument("command", help="please input command 'list' or 'del'")
args = parser.parse_args()

#
# Conf file
#
CONFIG_FILE = WORKDIR + FOLDER_SIG + 'etc' + FOLDER_SIG + 'ftps.conf'

targetList = []

#
# program function. 
#
def get_auth_info(conf_path):

    if conf_path is None:
        HOST = myftps.get_ftps_HOST()
        ACCOUNT = myftps.get_ftps_USER()
        PASSWORD = myftps.get_ftps_PASS()
    else:
        HOST = myftps.get_ftps_HOST(conf_path)
        ACCOUNT = myftps.get_ftps_USER(conf_path)
        PASSWORD = myftps.get_ftps_PASS(conf_path)

    return HOST, ACCOUNT, PASSWORD

def get_ftp_target_list(conf_path):

    TARGET_LIST_DIR = myftps.get_ftps_FTP_DEL_LIST_DIR()
    TARGET_LIST_FILE = myftps.get_ftps_FTP_DEL_LIST_FILE()

    if TARGET_LIST_DIR is None: LARGET_LIST_DIR = ""
    if TARGET_LIST_FILE is None: LARGET_LIST_FILE = ""

    return TARGET_LIST_DIR, TARGET_LIST_FILE


if __name__ == '__main__':
    #
    #logging
    #
    LOGGING_FILE = myftps.get_LOG_FILE(CONFIG_FILE)
    LOGGING_LEVEL = myftps.get_LOG_LEVEL(CONFIG_FILE)

    logging.basicConfig(filename=LOGGING_FILE, level=logging.DEBUG)
    #console output message level is info.
    #default(file) message level is debug.
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(name)-20s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

    #main module logger
    logger_main = logging.getLogger(__name__)


    logger_main.info('%s program start.', datetime.datetime.now())

    #load setting
    FTP_HOST,FTP_ACCOUNT,FTP_PASSWORD = get_auth_info(CONFIG_FILE)
    FTP_DIR = myftps.get_ftps_FTP_LOGIN_DIR(CONFIG_FILE)

    #get file candidate list
    FTP_LIST_DIR, FTP_LIST_FILE = get_ftp_target_list(CONFIG_FILE)
    FTP_LIST_DIR = WORKDIR + FOLDER_SIG + FTP_LIST_DIR
    FTP_LIST_FILE = WORKDIR + FOLDER_SIG + FTP_LIST_FILE


##### editing... #####
    if args == "list":
        



