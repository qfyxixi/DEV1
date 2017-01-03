
## Export Data##

Only need 4 steps, you can complete it.  
- prepare  
- creat connect  
- pack  
- send mail  


### 1.prepare ###

code

---
	import datetime
	import glob
	import MySQLdb
	import os, os.path
	import smtplib
	import tarfile #package
	import sys
	reload(sys)
	sys.setdefaultencoding('utf-8')
	from ConfigParser import ConfigParser
	from email.MIMEText import MIMEText
	from email.MIMEMultipart import MIMEMultipart

	project_name = 'heal'
	pwd_file    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/'+project_name+'/heal.cfg'
	timestamp = datetime.datetime.today().strftime("%Y%m%d%H%M%S")

---

configuration 

---
	[sql]
	sql1=xxx
	sql2=xxx
	sql3=xxx
	sql4=xxx
	sql5=xxx


	[mail]
	address_to = xx@xx.com

	[db]
	user = xx
	password = xxx
	host = xxx.xx.xx.xx
	port = 3306
	schema = tablename

---

### 2.get the conneting infomation,create one connect ###

---
	# read data from configfile,connect database,excute query sql,write into the file
	# get the conneting infomation,create one connect
    def db_info():
	config = ConfigParser()
	config.read(pwd_file)
	db_user = config.get('db', 'user')
	db_pwd = config.get('db', 'password')
	db_host = config.get('db', 'host')
	db_port = int(config.get('db', 'port'))
	db_schema = config.get('db', 'schema')
	db = MySQLdb.connect(user=db_user, passwd=db_pwd, host=db_host, port=db_port, db=db_schema, charset='utf8')

	# get sql,excute query sql
	list_sql = config.options('sql')
	for sql in list_sql:
		file_name = '/tmp/'+sql+'_'+timestamp+'.csv'
		f = open(file_name, 'w')
		cur = db.cursor()
		exec_sql = config.get('sql', sql)
		cur.execute(exec_sql)
		line_desc = ''
		for desc in cur.description:
			desc = str(desc[0])
		desc = desc.replace(r'，','_')
			desc = desc.replace(r',','_')
			desc = desc.replace(r'\r\n','')
			desc = desc.replace(r'\r','')
			desc = desc.replace(r'\n','')
		desc = desc.rstrip()
			line_desc = line_desc + desc+ ','
		line_desc = line_desc.rstrip(',').encode('utf8')
		f.write(line_desc)
		f.write(os.linesep)
		
		# write into the file
		for row in cur.fetchall():
			line = ''
			for cell in row:
				cell = str(cell)
				desc = desc.replace(r'，','_')
				desc = desc.replace(r',','_')
				desc = desc.replace(r'\r\n','')
				desc = desc.replace(r'\r','')
				desc = desc.replace(r'\n','')
				desc = desc.rstrip()
				line = line+cell+','
			line = line.rstrip(',').encode('utf8')
			f.write(line)
			f.write(os.linesep)
		cur.close()
		f.close()
	db.commit()
	db.close()

---

### 3.pack files ###
---
	def tar_file():

	# scan file .csv under the /tmp,then pack '''
	tar_filename = 'sql_'+timestamp+'.tar.gz'
	os.chdir('/tmp')
	t = tarfile.open(tar_filename, 'w:gz')
	for i in glob.glob('*.csv'):
		t.add(i)
		os.remove(i)
	t.close()

---

### 4.send mail ###
---
	def email():
	
	#change to the file location
	config = ConfigParser()
	config.read(pwd_file)
	address_to = config.get('mail', 'address_to')
	os.chdir('/tmp')
	tar_filename = 'sql_'+timestamp+'.tar.gz'
	
    #Determine the file size,Its size must less than 5242880
	msg = MIMEMultipart()
	if os.path.getsize(tar_filename) > 5242880:
		is_att = 1
		body = 'Failure! The file is too large.Data export fail.If you have any question,please contact xxx or send mail to the RD'
	else:
		is_att = 0
		body = 'Success!Data export succeed.If you have any question,please contact xxx or send mail to the RD'
   
    #send mail
	if is_att == 0:
		msg.attach(MIMEText(body, 'html', 'utf8'))
		att = MIMEText(open(tar_filename, 'rb').read(), 'base64', 'utf8')
		att["Content-Type"] = 'application/octet-stream'
		att["Content-Disposition"] = 'attachment; filename="%s"' % (tar_filename)
		msg.attach(att)
	to_email = address_to
	from_email = 'db-request@qunar.com'
	msg['to'] = to_email
	msg['from'] = from_email
	msg['subject'] =  'export data.'+timestamp+'By:xx'
	s_msg = smtplib.SMTP('localhost')
	s_msg.sendmail('', to_email.split(','), msg.as_string('Ture'))
	s_msg.quit()
	
    # delete files
	os.remove(tar_filename)

---

### main function###
---
	if __name__ == "__main__":
	db_info()
	tar_file()
	email()

---
