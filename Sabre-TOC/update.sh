#!/bin/bash

sd=`pwd`
cd ~/sabre/Sabre-TOC/

git pull

sudo /bin/cp -rf ./* /opt/Sabre-TOC/

cd $sd
