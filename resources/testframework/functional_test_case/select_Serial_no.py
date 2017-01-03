import datetime
import glob
import MySQLdb
import os, os.path
import smtplib
import tarfile
import sys
def select_Serial_no():
    conn=MySQLdb.connect(host='xx.xx.xx.xx',user='root',passwd='xxx',db='roomcontrol',port=3306)
    cursor=conn.cursor()    
    sql4 = "SELECT serial_no FROM `oo_order` ORDER BY DT_CREATED DESC LIMIT 1;"
    cursor.execute(sql4)
    for row in cursor.fetchall():
        Serial_no=row[0]     
        break
    conn.commit()
    cursor.close()
    conn.close()
    return Serial_no
