# -*- coding: utf-8 -*-
"""
Created on Fri Nov 21 14:07:31 2014

@author: user
Шаг 1 -- обнавление базы
    подшаг 1 -- подключение к фтп
    подшаг 2 -- проверка статуса
    подшаг 3 -- обнавление 
Шаг 2 -- подготовка
Шаг 3 -- запуск SAS (R) скриптов

"""
import os
from ftplib import FTP
import time
import datetime

path = "D:\AC\DBMirror\ "
logmsg = '\nStart session at '
lastupdate = {}

ts = time.time()
logmsg += datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
logmsg += '\n'

try:
    ftp = FTP("86.62.114.205")
    ftp.login("Ftpuser2", "")
    
    listing = []
    ftp.retrlines("LIST", listing.append)
    words = [i.split(None, 8) for i in listing]
    lastupdate =  {i[-1].lstrip():'_'.join(i[5:8]) for i in words}
    logmsg += 'Last updates:\n'
    logmsg +=  ''.join([str(i)+' = '+str(lastupdate[i])+'\n' for i in lastupdate])
    
    logmsg += 'Start update process\n'
    for bases in lastupdate:
        d = path + str(bases) +'\ '+ lastupdate[bases]
        if not os.path.exists(d):
            os.makedirs(d)
            logmsg += str(bases)
            logmsg += ' -- UPDATE\n'
            ftp.cwd(bases)
            l = []
            ftp.retrlines("LIST", l.append)
            w = [i.split(None, 8) for i in l]
            lfn = [i[-1].lstrip() for i in w]
            for i in lfn:
                lf = open(str(d) + '\ '+str(i), "wb")
                ftp.retrbinary("RETR " + str(i), lf.write)
                lf.close()
            ftp.cwd('..')
            logmsg += 'DB successful updated\n----------------------------------'
        else:
            logmsg += str(bases)
            logmsg += ' -- NO UPDATES\n'
            
    ftp.cwd('OL')
    
except BaseException as a:
    logmsg += str(a.args)
  
  
#listing = []
#ftp.retrlines("LIST", listing.append)

#logging
log = open(path+'log.txt', 'a')
log.write(logmsg)
log.close()
#fp.close()


ftp.close()