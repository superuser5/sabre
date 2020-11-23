#!/bin/bash

#setup installer to run and place output into a log file

chmod +x ./fedora-install.sh &
chmod +x ./install.sh &

mkdir ~/.sabre 2&> /dev/null

#sudo mkdir /opt/Sabre-TOC
#sudo cp -R ~/sabre/Sabre-TOC/* /opt/Sabre-TOC/

read -p 'Do you have an existing SSH key for this user account?: (Y/N)' s
if [ $s == 'Y' ]; then
	echo 'Using existing SSH key for TOC access' 
elif [ $s == 'y' ]; then
	echo 'Using existing SSH key for TOC access'
elif [ $s == 'N' ]; then 
	echo 'We need to create a key pair now. Select ALL DEFAULTS! After creating it you will need to copy it to your AP by copying it out of this terminal and pasting it on your AP.'
	#ssh-keygen
	#cat ~/.ssh/id_rsa.pub > ~/.ssh/authorized_keys
	#cat ~/.ssh/id_rsa
	echo 'Copy the key above and paste it into a file on your local machine. Hit Enter to continue.'
	read -p '' u
elif [ $s == 'n' ]; then
	echo 'We need to create a key pair now. Select ALL DEFAULTS! After creating it you will need to copy it to your AP. by copying it out of this terminal and pasting it on your AP.'
	#ssh-keygen 
	#cat ~/.ssh/id_rsa.pub > ~/.ssh/authorized_keys
	#cat ~/.ssh/id_rsa
	echo 'Copy the key above and paste it into a file on your local machine. Hit Enter to continue.'
	read -p '' u
fi

read -p '1 for RHEL installer, 2 for Debian installer: ' v
#read -p 'Is there a proxy? If so whats the URL: ' p

if [ $v -eq 1 ] ; then
	cp /opt/sabre/Sabre-TOC/main-init-scripts/main-RHEL.py /opt/sabre/Sabre-TOC/main.py
	cd /opt/sabre/Sabre-TOC/
	sudo ./fedora-install.sh |& tee -a fedora-install.log
elif [ $v -eq 2 ]; then
	cp /opt/sabre/Sabre-TOC/main-init-scripts/main-debian.py /opt/sabre/Sabre-TOC/main.py
	cd /opt/sabre/Sabre-TOC/
	sudo ./install.sh |& tee -a install.log
else
	echo "Either 1 or 2 please"
	exit
fi
