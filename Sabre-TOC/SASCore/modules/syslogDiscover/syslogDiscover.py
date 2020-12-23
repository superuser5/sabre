#!/usr/bin/python3


from scapy.all import *
import sys
import time

class readpcap():

    def __init__(self, capf, sysArgv2):
        self.pcapfile = capf
        self.sysArgv2 = sysArgv2

    def helpme():
        print '''
        usage: syslogDiscover <PCAP FILE TO PARSE> <Suspected SYSLOG PORT>
        '''
        quit()


    def parseme(self, pcapfile, sysArgv2):

        try:
            packets = rdpcap(pcapfile)
        except:
            print '''
            Error loading pcap file. Try again
            '''
            quit()

        pU = 'false'
        pT = 'false'
        pA = 'false'
        aP = []

        syslogServer = []
        syslogClient = []
        abnormSend = []
        abnormRecv = []


        t = len(packets) - 1
        c = 0

        print '''
################################################################
   This Tool assumes that the pcap has only syslog ports used
       It also does not handle IPv6 traffic well.
################################################################

    LOADING..................................
        '''
        time.sleep(10)

        for i in packets:
            p = packets[c][Ether].summary()
            if p.split()[0] != "Ether":
                continue
            if p.split()[4] == "UDP":
                pU = 'true'
            elif p.split()[4] == "TCP":
                pT = 'true'
            else:
                pA = 'true'
            #try:
            ps7 = p.split()[7]
            #except:
            #    ps7 = 'unknown:unknown'
            try:
                ps7.split(':')[1]
            except:
                #ps7 = str(ps7) + ':%s' % ps7
                ps7 = 'unknown:unknown'
                #print ps7
            try:
                ps5 = p.split()[5]
            except:
                ps5 = 'unknown'
            if p.split()[6] == 'DNS':
                ps7 = 'DNS-Traffic:DNS'
                ps5 = 'DNS'
            if p.split()[2] == 'ARP':
                ps7 = 'ARP-Traffic:ARP'
                ps5 = 'ARP'
            if p.split()[4] == 'ICMP':
                ps7 = '0.0.0.0-ICMP:ICMP'
                ps5 = 'ICMP'
            if p.split()[2] == '::':    
                ps5 = 'IPv6'
                ps7 ='IPv6-ADDR:IPv6'
            if p.split()[2] == 'IPv6':
                ps5 = 'IPv6'
                ps7 = 'IPv6-ADDR:IPv6'
            if p.split()[2].split(':')[0] == 'fe80':
                ps5 = 'IPv6'
                ps7 = 'IPv6-ADDR:IPv6'
            #print p.split()
            #print ps7
            try:
                aP.append(ps7.split(':')[1])
            except:
                aP.append('unknown')
            if pU =='true' or pT == 'true':
                if ps7.split(':')[1] == 'syslog' or ps7.split(":")[1] == str(sysArgv2):
                    syslogClient.append(p.split()[5])
                    syslogServer.append(ps7)
                else:
                    aP.append(ps7.split(':')[1])
                    if ps5 != 'DNS'and ps5 != 'ARP' and ps5 != 'ICMP' and ps5 != 'IPv6':
                        abnormRecv.append(ps7)
                        abnormSend.append(ps5)
            else:
                if ps5 != 'DNS' and ps5 != 'ARP' and ps5 != 'ICMP' and ps5 != 'IPv6':
                    abnormRecv.append(ps7)
                    abnormSend.append(ps5)
                    aP.append(ps7.split(':')[1])
            c = c + 1
    
    
        syslogServer = list(set(syslogServer))
        syslogClient = list(set(syslogClient))
        abnormSend = list(set(abnormSend))
        abnormRecv = list(set(abnormRecv))
        aP = list(set(aP))
    
        print '''
    

        '''    
    
        print '''
################################
   Layer 2 Protocols Detected
################################
        '''

        if pU == 'true':
            print "UDP Protocol Detected"
        if pT == 'true':
            print 'TCP Protocol Detected'
        if pA == 'true':
            print "Non-TCP or UDP Protocols Detected"

        print '''
#####################################
   Actual PORTS/Protocols Detected
#####################################
        '''
        if len(aP) > 0:
            for i in aP:
                print i

        print '''
###########################################
   Possible Syslog Forwarders or Clients
###########################################
        '''
        for i in syslogClient:
            print i

        print '''
#################################################
   Possible Syslog Server or Aggregation Hosts
#################################################
        '''
        for i in syslogServer:
            print i

        print '''
################################################
   Possible Abnormal Traffic Producing Hosts
################################################
        '''
        for i in abnormSend:
            print i

        print '''
################################################
   Possible Abnormal Traffic Recieving Hosts
################################################
        '''
        for i in abnormRecv:
            print i

        print '''


        '''

def main(pcapf):
    pcapData = readpcap()
    pcapData.parseme(pcapf)

def helpme():
    print '''
    usage: syslogDiscover <PCAP FILE TO PARSE>
    '''
    quit()

if __name__ == "__main__":
    print '''
This Tool was developed to identify Splunk instances on the network with out network scanning tools such as:
        -nmap
        -zenmap
        -etc...

    This sould be ran with a PCAP file generated filtering only for SYSLOG traffic port 514

    Example: tcpdump -s 65535 -i ens33 port 514 -w syslog-514.pcap

    Author: Austin James Scott
    Email: austin.j.scott@lmco.com

    '''
    if len(sys.argv) < 3:
        sysArgv2 = '514'
    else:
        sysArgv2 = sys.argv[2]
    if len(sys.argv) < 2:
        helpme()
    if sys.argv[1] == '-h':
        helpme()
    TCP_REVERSE = dict((TCP_SERVICES[k], k) for k in TCP_SERVICES.keys())
    try:
        sysArgv2 = TCP_REVERSE[int(sysArgv2)]
    except:
        print "Error: That port wasn't in the SCAPY service list"
        quit()
    pcapf = sys.argv[1]
    try:
        main(pcapf)
    except:
        "error... try again"




