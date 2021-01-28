#!/bin/bash

pip install pexpect

sd=`pwd`
sudo mkdir /opt/Sabre-Cli
sudo /bin/cp -R ./* /opt/Sabre-Cli/
sudo ln -s /opt/Sabre-Cli/Sabre-Web/Sabre-Cli/pssh.py /usr/bin/sabre-cli
sudo ln -s /opt/Sabre-Cli/Sabre-Web/sabre-web.sh /usr/bin/sabre-web

cd /opt/Sabre-Cli/Sabre-Web/
python3 -m venv server
/opt/Sabre-Cli/Sabre-Web/server/bin/pip install -r ./requirements.txt

echo '''

###############################################################
#                                                             #
#                     #####################                   #
#                     # INSTALL COMPLETE! #                   #
#                     #####################                   #
#                                                             #
# Run "sabre-cli -u {Sabre User} -s {Sabre-TOC IP or Domain}" #
# Run "sabre-web {Give a username and server to connect to}"  #
#	- Then connect to http://127.0.0.1:5000		      #
#                                                             #
###############################################################

'''
