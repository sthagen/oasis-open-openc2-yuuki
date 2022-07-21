# Yuuki
## Linux Set-Up Instructions

* Python3+
  * latest python version comes with most Linux systems:  
&ensp;&ensp;`python3 --version`
  * python3.8-distutils:  
&ensp;&ensp;`sudo apt install python3.8-distutils`
* Pip3:  
&ensp;&ensp;`sudo apt install python3-pip`  
&ensp;&ensp;`pip3 --version`
* A Virtual Environment package, these instructions are geared for VirtualEnvWrapper

* Make sure you have Git installed and updated.  
&ensp;&ensp;`sudo apt update`  
&ensp;&ensp;`sudo apt install git`  
&ensp;&ensp;`git --version`  

## Install Yuuki

1. Clone the OpenC2 Yuuki Repository:  
&ensp;&ensp;`git clone https://github.com/oasis-open/openc2-yuuki.git`  
or our dev version:  
&ensp;&ensp;`git clone https://github.com/ScreamBun/openc2-yuuki.git`

3. Create the Yuuki virtual environment in the Yuuki folder:  
&ensp;&ensp;`mkvirtualenv yuukienv`  
Note: after the initial build, you only need to run the following command:  
&ensp;&ensp;`workon yuukienv`

4. Create build folder:  
&ensp;&ensp;`python3 -m pip install -U -r requirements.txt /home/<<your-name>>/.virtualenvs/<<your-virtual-env>>/lib/python3.10/site-packages`

5. Run setup.py  
&ensp;&ensp;`python3 setup.py develop /home/<<your-name>>/.virtualenvs/<<your-virtual-env>>/lib/python3.10/site-packages`

6. Install Actuator Specific tools (If Applicable):  
OSQuery ORM (used in some examples- not required for Yuuki to function):  
&ensp;&ensp;`python3 -m pip install git+https://github.com/ScreamBun/SB_utils.git#subdirectory=osquery_orm`  
In `yuuki/examples/actuators/osquery_conf.ini`, rename file path to YOUR file path    
Note: To find the name of the machine, run the following command:  
&ensp;&ensp;`whoami`  
If it'92s missing, create the file.  
**Filename:**  
&ensp;&ensp;`osquery_conf.ini`  
**Contents:**  
&ensp;&ensp;`[osquery]`  
&ensp;&ensp;`socket: /Users/<your-name>/.osquery/osqueryd.sock`

## Run Example File using Yuuki:
1. Go to Yuuki root
2. Run:  
&ensp;&ensp;`workon yuukienv`
3. Kick off an example:  
&ensp;&ensp;`python3.8 examples/mqtt_consumer_plugfest.py`