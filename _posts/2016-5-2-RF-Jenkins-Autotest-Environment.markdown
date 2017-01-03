## Build ci auto test environment ##
-create local robotFramework test environment  
-create server robotFramework test environment  
-bulid CI environment

### 1.create local robotFramework test environment ###
1)https://pypi.python.org/pypi/robotframework  
2)python setup.py install  
3)pybot --version


### 2.create server robotFramework test environment ###
1)install gcc  
```yum install -y bzip2* gcc-c++```  

2)install make  
```yum -y install gcc automake autoconf libtool make```    

3)unzip install package  
```tar -zxvf Python-2.7.6.tgz```  

4)config excute path  

---
	cd Python-2.7.6
	./configure --prefix=/usr/local/python2.7.6

---

5)install python  
```make && make install```  
tips:If you meet the questionas following:  
/usr/bin/install: cannot create directory `/usr/local/python2.7.6': Permission denied  
slove:  
sudo chown -R 'whoami' /usr/local  

6) verify install result  
```sudo /usr/local/python2.7.6/bin/python2.7 ```  

7)Usually system has its own python ,you need to make a copy.  

---
	mv /usr/bin/python /usr/bin/python2.6.6
	vi /usr/bin/yum

---  
change the first line from:  
!/usr/bin/python  
to  
!/usr/bin/python2.6.6  

8)make a soft link  
```sudo ln -s /home/q/robot/python2.7.6/bin/python2.7 /usr/bin/python```  

9)verify the default python version  
```python -v```  

10)install pip  

---
	wget --no-check-certificate https://pypi.python.org/packages/source/s/setuptools/setuptools-1.4.2.tar.gz
	tar -xvf setuptools-1.4.2.tar.gz 
	cd setuptools-1.4.2  
	python2.7 setup.py install
	sudo wget --no-check-certificate https://raw.githubusercontent.com/pypa/pip/master/contrib/get-pip.py
	python get-pip.py
	vi  /etc/profile
	export PATH=$PATH:$JAVA_HOME/bin:/usr/local/python2.7.6/bin  
	source /etc/profile

---

11)install easy_install
 
--- 
	wget -q http://peak.telecommunity.com/dist/ez_setup.py
    python ez_setup.py
	easy_install --version

---

12)install robotframework  
```pip install robotframework==2.8.4```  

13)install RF-library  

---
	sudo easy_install robotframework-selenium2library
	sudo easy_install robotframework-httplibrary

---

14)install mysql  
```sudo pip install MySQL-python```  

15)find the install path  
```sudo find / -name "*robotframework*" | grep --color robotframework```  

refrence:[Common Python Tools: Using virtualenv, Installing with Pip, and Managing Packages](https://www.digitalocean.com/community/tutorials/common-python-tools-using-virtualenv-installing-with-pip-and-managing-packages)

### 3.bulid CI environment ###
1)create jobs on the jenkins,open hook (connect git and jenkins)  
2)create shell for running the testing  
3)set rc testing action after buliding on the jenkins


