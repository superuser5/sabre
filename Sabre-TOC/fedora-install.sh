#!/bin/bash
clear
echo '''
Run as ROOT!!! and Requires MSF and Empire to be installed before hand for now.
MSF and Empire will be added to the installer soon!
'''

sd=`pwd`
#export http_proxy = $1
#export https_proxy = $1
#git config --global http.proxy $1

#add-apt-repository -y ppa:webupd8team/java

yum -y update
sleep 2
yum -y install epel-release
sleep 2
yum -y install redis.x86_64 python-redis openssh-server nmap git python2-pip # oracle-java8-installer if we add MSF back to the main installer
sleep 2
yum -y install python-cmd2 python-flask python-iptools python-netifaces
python-pexpect python2-scapy
sleep 2
#yum update
yum -y upgrade
sleep 2
yum -y install build-essential libreadline-dev libssl-dev libpq5 libpq-dev
libreadline5 libsqlite3-dev libpcap-dev git-core autoconf postgresql pgadmin3
curl zlib1g-dev libxml2-dev libxslt1-dev vncviewer libyaml-dev curl zlib1g-dev
screen tmux moreutils
sleep 1

echo '''
###################################
# Installing Metasploit Framework #
###################################

'''
cd /opt
curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > msfinstall && \
  chmod 755 msfinstall && \
  ./msfinstall
cd ~

#echo '''

################################
# Installing Powershell Empire #      This will be changed to install from PTF
################################
#
#'''

cd /opt
git clone https://github.com/EmpireProject/Empire.git
cd Empire
wget http://dl.fedoraproject.org/pub/fedora/linux/releases/27/Everything/x86_64/os/Packages/p/python2-pydispatcher-2.0.5-2.fc27.noarch.rpm
rpm -i python2-pydispatcher-2.0.5-2.fc27.noarch.rpm
pip install zlib_wrapper macholib dropbox pyminifier 
chmod +x ./setup/install.sh
./setup/install.sh
ln -s /opt/Empire/empire /usr/bin/empire
cd ~


echo ''

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

sed -i 's/PermitRootLogin\ prohibit-password/PermitRootLogin\ without-password/' /etc/ssh/sshd_config
service ssh restart

echo '''

#############################################################
# Accept the defaults for the SSH key about to be generated #
#############################################################

'''
sleep 5
ssh-keygen

cat /root/.ssh/id_rsa.pub > /root/.ssh/authorized_keys
cp /root/.ssh/id_rsa ./TSKEY
chmod 600 TSKEY
echo '''

########################################
# Copy the TSKEY to use on your AP!!!! #
########################################

'''
sleep 3

pip install --upgrade pip

pip install pexpect
pip install scapy

#snap install rocketchat-server

d=`pwd`
ln -s $d/SASCore/Listeners/simple.py /usr/bin/simple.py
ln -s $d/s-cli.py /usr/bin/sabre
echo -n '''

PLEASE SPECIFY AN IP FOR THE TOC TO LISTEN FOR APs ON:

'''
read ip
sed -i “s/bind\ 127.0.0.1/bind\ 0\.0\.0\.0/“ /etc/redis/redis.conf

sed -i “s/localhost/0\.0\.0\.0/“ $d/SASCore/Listeners/settings.py

systemctl enable redis
systemctl start redis
redis-server &
sleep 5
echo '''

########################################################
# Redis server running! TOC stood up and ready for Ops #
#      Dont forget to copy TSKEY over to your AP!      #
########################################################

'''

