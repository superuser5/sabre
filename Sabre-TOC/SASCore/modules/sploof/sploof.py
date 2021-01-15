#!/usr/bin/python3

from scapy.all import *

# usage: $0 <target ip> <message>

from scapy.all import *
import sys
import time

class sendMe():

    def udpSend(self, t, m, uP):
        for prio in range(0, 7):
            for faci in range(0, 23):
                priority = (prio << 3) | faci
                syslog = IP(dst=t)/UDP(dport=uP)/Raw(load='<' + str(priority) + '>' + time.strftime("%b %d %H:%M:%S ") + m)
                send(syslog, verbose=0)
                sys.stdout.write(".")
                sys.stdout.flush()

        print("")

    def tcpSend(self, t, m, tP):
        for prio in range(0, 7):
            for faci in range(0, 23):
                priority = (prio << 3) | faci
                syslog = IP(dst=t)/TCP(dport=tP)/Raw(load='<' + str(priority) + '>' + time.strftime("%b %d %H:%M:%S ") + m)
                send(syslog, verbose=0)
                sys.stdout.write(".")
                sys.stdout.flush()
    
        print("")

def helpMe():
    print('''

  Usage: syslogFuzz.py <Target IP> <Message> <Port> <TCP or UDP> <-f or --fuzz OPTIONAL>

Example: python syslogFuzz.py 192.168.52.131 "Feb 23 07:55:01 ubuntu CRON[49988]: pam_unix(cron:session): session opened for user root by (uid=0)" -u 514 -f

  or

Example: python syslogFuzz.py 192.168.52.131 "Z owes me a beer" -u 514 -f

    ''')
    quit()

def main(mt, mm, po, p):
    fuzz = sendMe()
    if p == '-t':
        fuzz.tcpSend(str(mt), str(mm), int(po))
    elif p == '-u':
        fuzz.udpSend(str(mt), str(mm), int(po))
    else:
        print('You need to specify tcp or udp. Using UDP')
        fuzz.udpSend(str(mt), str(mm), int(po))


if __name__ == "__main__":
    print('''
    This Tool was developed to fuzz syslog traffic into Splunk instances on the network.

    Example: syslogFuzz.py <target ip> <message> <port> <TCP or UDP> <-f or --fuzz OPTIONAL>
        
        -t              == TCP
        -u              == UDP
        -f  or --fuzz   == Optionally Fuzz by Generating Large Messages to the Server

    TODO:
        - Add Spoofing of Source capability
        - Add greater fuzzing capability (currently limited to use typed messages and message size testing)

    Author: Austin James Scott
    Email: austin.j.scott@lmco.com

    ''')
    try:
        target = str(sys.argv[1])
    except:
        print('Error argv[1]')
        helpMe()
    try:
        msg = str(sys.argv[2])
    except:
        print('Error argv[2]')
        helpMe()
    try:
        p = str(sys.argv[3])
    except:
        print('Error argv[3]')
        helpMe()
    try:
        portN = str(sys.argv[4])
    except:
        print('Error argv[4]')
        helpMe()
    if len(sys.argv) == 6:
        if sys.argv[5] == '--fuzz' or sys.argv[5] == '-f':
            try:
                while True:
                    msg = str(msg) + str(msg)
                    print(str(len(msg)) + " Characters being sent")
                    #print target + msg + portN + p
                    main(target, '%s' % msg, portN, p)
            except:
                print('Fuzz fail')
                quit()
    try:
        print(target + ' ' + '"' + msg + '"' + ' ' + p + ' ' + portN)
        main(sourceIP, target, "%s" % msg, portN, p)
    except:
        "error... try again"


