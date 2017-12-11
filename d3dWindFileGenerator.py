#!/usr/bin/python
# -*- coding: UTF-8 -*-
import MySQLdb
from lxml import etree
from datetime import *

#Database details. For MySQL database. For different DB or file, should be changed
HOST = 'localhost'
USER = 'user'
PASS = 'pass'
DB   = 'database'

def createWindFile(dateIni, dateFin, steps):
    """
        Create a file with wind values as .wnd file of Delft3D from CdP database
        In: "Start date, end date, timestep"
        Out: File: .wnd
    """
    db = MySQLdb.connect(host = HOST, user = USER, passwd = PASS, db = DB)
    cursor = db.cursor()
    #Si el limite inferior y superior es 0, se calcula la desviacion estandar para el calculo de picos
    #V1 sql = 'SELECT TIMESTAMPDIFF(MINUTE, %s, VaisalaWind.date), Sm, Dm FROM VaisalaWind where date between %s and %s' % (dateIni, dateIni, dateFin)
    sql = 'SELECT TIMESTAMPDIFF(MINUTE, %s, VaisalaWind.date), AVG(Sm), AVG(Dm) FROM Wind where date between %s and %s GROUP BY DATE(date), ((60/10) * HOUR (TIME(date)) + FLOOR(MINUTE(TIME(date)) / 10)) ORDER BY date' % (dateIni, dateIni, dateFin) #Example
    print "%s" % sql
    cursor.execute(sql)
    result = cursor.fetchall()
    i = 0;
    filename = 'Wind%s%s.wnd' % (dateIni, dateFin)
    f = open(filename,"w")
    
    for item in result:
        if i%steps == 0:
            f.write("%d. %f %d.\n" % (result[i][0], result[i][1], result[i][2]))        
        i = i + 1
    
    f.close()

def main():
	print "Running wind"   
        #Input: Start date, end date, timestep
	createWindFile("'2014-04-01 00:00:00'", "'2014-11-30 00:00:00'",1)
               
if __name__ == "__main__":
    main()
    
