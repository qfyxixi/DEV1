import datetime
import glob
import MySQLdb
import os, os.path
import smtplib
import tarfile
import sys
def selectActionId():
    conn=MySQLdb.connect(host='xx.xx.xx.xx',user='root',passwd='xx',db='tablename',port=3306)
    cursor=conn.cursor()    
    sql4 = "SELECT * FROM`rc_lock_card_status` ORDER BY id DESC LIMIT 1;"
    cursor.execute(sql4)
    for row in cursor.fetchall():
        citycode=row[3]     
        break
    conn.commit()
    cursor.close()
    conn.close()
    return citycode




