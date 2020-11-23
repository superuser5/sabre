#!/bin/bash

echo ''' RUN AS ROOT!!!!'''

apt-get update
apt-get install -y python-redis python-pip terminator stunnel4

pip install --upgrade pip
pip install cmd2
pip install notify2
pip install pexpect


sd=`pwd`

mkdir ~/.config/terminator/
cp $sd/config ~/.config/terminator/config
mkdir /etc/Sabre/
cp $sd/settings.py /etc/Sabre/
cp $sd/sabres.txt /etc/Sabre/
cp $sd/redis-stunnel.conf /etc/stunnel/

read -p 'Due to an issue with the installer you will need to update the TOC (SERVER) IP listed in the /etc/stunnel/redis-stunnel.conf file. Then run "/etc/init.d/stunnel start"' ip

ln -s $sd/sshconn.py /usr/bin/sshconn
ln -s $sd/pub.py /usr/bin/pub
ln -s $sd/sub.py /usr/bin/sub
ln -s $sd/startOp /usr/bin/sabre-cli

echo '''

###################################################
#                                                 #
#              #####################              #
#              # INSTALL COMPLETE! #              #
#              #####################              #
#                                                 #
#    Place TSKEY from Sabre-TOC in /etc/Sabre/    #
#      Also 'chmod 600 TSKEY' before running      #
# Place private.pem from Sabre-TOC in /etc/Sabre/ #
#   Also 'chmod 600 private.pem' before running   #
#                                                 #
###################################################

'''
