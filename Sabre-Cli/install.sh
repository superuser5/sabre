#!/bin/bash

pip install pexpect

sd=`pwd`
sudo mkdir /opt/Sabre-Cli
sudo /bin/cp -R ./* /opt/Sabre-Cli/
sudo ln -s /opt/Sabre-Cli/Sabre-Web/Sabre-Cli/pssh.py /usr/bin/sabre-cli
sudo ln -s /opt/Sabre-Cli/Sabre-Web/sabre-web.sh /usr/bin/sabre-web

echo '''

###############################################################
#                                                             #
#                     #####################                   #
#                     # INSTALL COMPLETE! #                   #
#                     #####################                   #
#                                                             #
# Run "sabre-cli -u {Sabre User} -s {Sabre-TOC IP or Domain}" #
#                                                             #
###############################################################

'''
