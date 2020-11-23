#!/usr/bin/python

from pexpect import pxssh
import getpass
import sys

try:
    s = pxssh.pxssh()
    hostname = sys.argv[1] #"66.45.251.148"
    username = sys.argv[2] #'root'
    password = sys.argv[3] #'Pq62sn5r!Pq62sn5r@Pq62sn5r%'
    s.login(hostname, username, password)
    print "Confirming Hostname: "
    s.sendline('hostname')
    s.prompt()
    print(s.before)
    print "Confirming User: "
    s.sendline('whoami')
    s.prompt()
    print(s.before)
    print "Starting Sabre. Use SHIFT-] to exit. This may takea few minutes........"
    s.sendline('sabre')
    s.prompt()
    print(s.before)
    fout = open('%s-sabre-cli.log' % hostname, 'wb')
    s.logfile = fout
    s.interact()
    print "\nClosed Sabre Connection!"
    s.logout
except pxssh.ExceptionPxssh as e:
    print("pxssh failed on login.")
    print(e)
