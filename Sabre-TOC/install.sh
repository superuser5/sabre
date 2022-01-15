#!/bin/bash
clear

#export http_proxy = $1
#export https_proxy = $1
#git config --global http.proxy $1
od=`pwd`
ip=`hostname -i | grep -v '127.0'`
sd='/opt/Sabre-TOC'

if [ -z $ip ]
then
	echo '''############################################
# No IP to set. Using 0.0.0.0 from now on. #
############################################'''
	ip='0.0.0.0'
fi


mkdir -p /home/root/.sabre/


apt update -y
sleep 2
apt install -y redis-server python-redis openssh-server nmap git python-pip3 openssh-server screen tmux moreutils python3-venv -y #oracle-java8-installer if we add MSF back to the main installer
sleep 2
apt upgrade
sleep 2
apt install -y build-essential libreadline-dev libssl-dev libpq5 libpq-dev libsqlite3-dev libpcap-dev git-core autoconf postgresql curl zlib1g-dev libxml2-dev libxslt1-dev libyaml-dev curl zlib1g-dev -y #pgadmin3 vncviewer libreadline5
sleep 1

echo '''

####################################
# Updating TMUX Conf file for ROOT #
####################################

'''

echo '''
set-option -g prefix C-a
unbind-key C-b
bind-key C-a send-prefix
''' >> /root/.tmux.conf

echo '''
* need to make this an option
#############################
# Installing TrustedSec PTF # 
#############################

'''

#cd /root/
#git clone https://github.com/trustedsec/ptf.git
#cd $sd


echo '''


###############################################
# Configuring other needed settings for Sabre #
###############################################

'''

#sed -i 's/PermitRootLogin\ prohibit-password/PermitRootLogin\ without-password/' /etc/ssh/sshd_config #commented this out for docker version
#service ssh restart

#debug
#sleep 3

pip3 install --upgrade pip3

pip3 install -r pip3-install-me.txt
#pip3 install covertutils
#pip3 install cmd2==0.7.9
#pip3 install pexpect
#pip3 install scapy

# need to make this optional
#snap install rocketchat-server

#Need to fix these SED commands
ln -s $sd/SASCore/Listeners/simple.py /usr/bin/simple.py
ln -s $sd/s-cli.py /usr/bin/sabre
ln -s $sd/update.sh /usr/bin/sabre-update
#sed -i “s/bind\ 127.0.0.1/bind\ 127.0.0.1\ $ip/“ /etc/redis/redis.conf

#debug
#sleep 3

#Need to fix this one as well
#sed -i “s/localhost/$ip/“ $d/SASCore/Listeners/settings.py

#debug
#sleep 3


#sed -i 's/localhost/$ip/' $d/SASCore//settings.py

systemctl enable redis
redis-server &
#cp /usr/bin/pip3 /usr/local/bin/pip3 #there is an issue with pip3 after install. something reaks pip3 in /usr/local/bin but the /usr/bin/ version works so I am replacing the local/bin one for now
sleep 5
echo '''

########################################################
# Redis server running! TOC stood up and ready for Ops #
#      Dont forget to copy TSKEY over to your AP!      #
########################################################

'''
