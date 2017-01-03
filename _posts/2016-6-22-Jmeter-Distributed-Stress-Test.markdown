## Jmeter distributed test ##

### principle ###
1. master + slave

2. Excute process：master send shell to the slave,slave get the shell to running test.

3. finish running:slave send the result to the slave,master collect all slave test result.

### slave configuration ###


1. install Jmeter

2. add environment variable  
	remote_hosts=10.13.223.202:1000,10.13.225.12:1000

3. start jmeter:   
```jmeter-server.bat```
4. save the endpoint infomation.

5. other slaves repeat step1-step4



### master configuration ###
1. creat a post shell

2. find the file:jmeter.properties 

3. open Jmeter，select running:  
	select 'Remote boot all machine',you can see the all slave test result on the master GUI  
	select 'Remote boot machine',you can see the slave test result on the Command line  interface

### Custom slave port ###
slave——jmeter.properties :change to the following

--- 
	server_port=1888
	server.rmi.localport=1888

---
master——jmeter.properties :  

---
	remote_hosts=10.13.223.202:1000,10.13.225.12:1000

---
restart jmeter.bat

### Other instructions ###



1. master and slave independence
2. Use the CSV parameter, you need to take a parameter file and the path to set the same copy on each slave 
3. The Jmeter versions and plug-ins installed on each machine are the same.