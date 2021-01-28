#!/bin/bash

cd /opt/Sabre-Cli/Sabre-Web/

read -p 'Username: ' user
read -p 'TOC Server: ' server

server/bin/python -m sabre-web --command sabre-cli --cmd-args "-u $user -s $server"
