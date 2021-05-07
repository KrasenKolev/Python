#! /usr/bin/env python3

## MIT License

## Copyright 2021 Krasen Kolev
#
## Permission is hereby granted, free of charge, to any person obtaining a copy
## of this software and associated documentation files (the "Software"), to deal
## in the Software without restriction, including without limitation the rights 
## to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
## copies of the Software, and to permit persons to whom the Software is 
## furnished to do so, subject to the following conditions:

## The above copyright notice and this permission notice shall be included in all 
## copies or substantial portions of the Software.

## THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
## IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
## FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL 
## THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
## LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
##  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
## SOFTWARE.

import sys
import getpass
from os import system
from netmiko import ConnectHandler
import re
from datetime import datetime

__version__ = 1.0

''' 
based on provided peer IP address this script will find:
1. The NAT'ed IP address
2. The access list (Encyption domain)
3. The crypto map 
then it will check the vpn status
- If the vpn is DOWN, it will notify the user that the VPN is DOWN and it prompt the user if he wants to reset the VPN.
- If the vpn is UP, it will notify the user that the VPN is UP and it prompt the user if he wants to reset the VPN anyway.
- If the vpn is UP, but there is not traffic moving on any of the SAs, it will notify the user that the VPN is UP, 
  but there is no traffic moving and it prompt the user if he wants to reset the VPN.

VPN reset is performed by clearing phase 1 and phase 2 sessions for the specified VPN peer IP. 

Script usage: ./vpnreset <FW hostname> <Peer IP>

NOTE: There are some RegEx's which needs to be adjusted according to everyones nameing conventions. Every position that needs to be adjusted is marked in the script. 
'''

try:
  if sys.argv[1] and sys.argv[2] != '':
    pass
except:
  print('No FW hostname has been provided!')
  print('Script usage: ./vpnreset <FW hostname> <Peer IP>')
  exit()


fw = sys.argv[1]
ip = sys.argv[2]

system('clear')

user = input('Please provide your username: ')
passwd = getpass.getpass('Please provide your password: ')

fw1 = fw + '!!! ADD DOMAIN NAME HERE !!!'
username = user
password = passwd

device = {
    'device_type': 'cisco_asa',
    'ip': fw1,
    'username': user,
    'password': passwd,
    'port': 22,
}
system('clear')
print('\nConnecting to firewall ' + fw + '...')

net_connect = ConnectHandler(**device)  

# 1 Search the running-config for the peer-address -> crypto map-number
# show running-config | include <Peer IP>

running_conf = net_connect.send_command('show running-config | include ' + str(ip))

CryptoMap = re.findall(r'REGEX', running_conf, re.I) !!! ADD REGEX HERE WHICH WILL MATCH THE CRYPTO MAP NUMBER  !!!

# 2. Search running-config for the crypto map number -> Crypto-ACL-name
# show running-config | include <CryptoMap number>

config_map = net_connect.send_command('show running-config | include ' + str(CryptoMap[0]))


ipsec = re.findall(r'REGEX', config_map)  !!! ADD REGEX HERE WHICH WILL MATCH THE VPN NAME !!!
ikeversion = re.findall(r'ikev[\d]', config_map)

print(50 * '#')
print('# Checking VPN: {:32} #'.format(ipsec[0]))

# 3. Get the remote IPs ( customer - host )Crypto-ACL
# show running-config access-list | include < customer name >

access_list = net_connect.send_command('show running-config access-list | include ' + str(ipsec[0]))

print(50 * '#')
print('The access list for VPN ' + ipsec[0] + ': \n' + access_list)

# 4. Display the NATed IPs

IPs = []
IPs = re.findall(r'\d+\.\d+\.\d+\.\d+', access_list)

regex = re.compile('25\d.\d+.\d+\.\d+')

filetered_list = [i for i in IPs if not regex.search(i)]

customer_IP = filetered_list[1]

print(50 * '#')
print('# Customer NAT IP is: {:26} #'.format(customer_IP))

nat_ip = net_connect.send_command('show nat ' + str(customer_IP) + ' detail')
print(50 * '#')
print('show nat ' + str(customer_IP) + ' detail \n' + nat_ip)

# 5. Verify the VPN status
timedate = datetime.now().isoformat(timespec='minutes')
vpnStatAftrRst = ''
vpnstatus = net_connect.send_command('show vpn-sessiondb detail l2l filter name ' + str(ip), delay_factor=4)
vpnpackets1 = net_connect.send_command('show vpn-sessiondb detail l2l filter name ' + str(ip) + ' | i Addr|Pkts ', delay_factor=4)
vpnpackets2 = net_connect.send_command('show vpn-sessiondb detail l2l filter name ' + str(ip) + ' | i Addr|Pkts ', delay_factor=4)

if vpnstatus == 'INFO: There are presently no active sessions of the type specified\n':
    vpndown = input('VPN {} is down, do you want to reset it ? N/y  '.format(ipsec[0]))
    if vpndown.lower() == 'y' or vpndown.lower() == 'yes':
      if ikeversion[0] == 'ikev1':
        vpnreset = net_connect.send_command('clear crypto ikev1 sa ' + ip)
        vpnreset += net_connect.send_command('clear crypto ipsec sa peer ' + ip)
        vpnStatAftrRst = net_connect.send_command('show vpn-sessiondb detail l2l filter name ' + str(ip))
        print('# VPN status after the reset:                    #')
        print(50 * '#')
        print(vpnStatAftrRst)
      elif ikeversion[0] == 'ikev2':
        vpnreset = net_connect.send_command('clear crypto ikev2 sa ' + ip)
        vpnreset += net_connect.send_command('clear crypto ipsec sa peer ' + ip)
        vpnStatAftrRst = net_connect.send_command('show vpn-sessiondb detail l2l filter name ' + str(ip))
        print('# VPN status after the reset:                    #')
        print(50 * '#')
        print(vpnStatAftrRst)
    else:
      print('VPN {} was NOT reset!'.format(ipsec[0]))
      print('quitting...')
      pass

elif 'Session Type: LAN-to-LAN Detailed' in vpnstatus and vpnpackets1 == vpnpackets2:
    print(50 * '#')
    print('# Status of the VPN:                             # ')
    print(50 * '#')
    print(vpnstatus)
    print(50 * '#')
    vpnup = input('VPN {} is UP, but either there is no or low traffic moving on ALL of the SAs! Do you want to reset the VPN ? N/y  '.format(ipsec[0]))
    print(50 * '#')
    if vpnup.lower() == 'y' or vpnup.lower() == 'yes':
      if ikeversion[0] == 'ikev1':
        vpnreset = net_connect.send_command('clear crypto ikev1 sa ' + ip)
        vpnreset += net_connect.send_command('clear crypto ipsec sa peer ' + ip)
        vpnStatAftrRst = net_connect.send_command('show vpn-sessiondb detail l2l filter name ' + str(ip))
        print('# VPN status after the reset:                    #')
        print(50 * '#')
        print(vpnStatAftrRst)
      elif ikeversion[0] == 'ikev2':
        vpnreset = net_connect.send_command('clear crypto ikev2 sa ' + ip, delay_factor=4)
        vpnreset += net_connect.send_command('clear crypto ipsec sa peer ' + ip, delay_factor=4)
        vpnStatAftrRst = net_connect.send_command('show vpn-sessiondb detail l2l filter name ' + str(ip), delay_factor=4)
        print('# VPN status after the reset:                    #')
        print(50 * '#')
        print(vpnStatAftrRst)
    else:
      print('VPN {} was NOT reset!'.format(ipsec[0]))
      print('quitting...')
      pass

elif 'Session Type: LAN-to-LAN Detailed' in vpnstatus:
    print(50 * '#')
    print('# Status of the VPN:                             # ')
    print(50 * '#')
    print(vpnstatus)
    print(50 * '#')
    vpnup = input('VPN {} is UP, do you want to reset it anyway ? N/y  '.format(ipsec[0]))
    print(50 * '#')
    if vpnup.lower() == 'y' or vpnup.lower() == 'yes':
      if ikeversion[0] == 'ikev1':
        vpnreset = net_connect.send_command('clear crypto ikev1 sa ' + ip)
        vpnreset += net_connect.send_command('clear crypto ipsec sa peer ' + ip)
        vpnStatAftrRst = net_connect.send_command('show vpn-sessiondb detail l2l filter name ' + str(ip))
        print('# VPN status after the reset:                    #')
        print(50 * '#')
        print(vpnStatAftrRst)
      elif ikeversion[0] == 'ikev2':
        vpnreset = net_connect.send_command('clear crypto ikev2 sa ' + ip)
        vpnreset += net_connect.send_command('clear crypto ipsec sa peer ' + ip)
        vpnStatAftrRst = net_connect.send_command('show vpn-sessiondb detail l2l filter name ' + str(ip))
        print('# VPN status after the reset:                    #')
        print(50 * '#')
        print(vpnStatAftrRst)
    else:
      print('VPN {} was NOT reset!'.format(ipsec[0]))
      print('quitting...')
      pass

net_connect.disconnect()

with open('Checks_for_VPN_' + ipsec[0] + '_on_FW_' + fw + '.txt', 'w') as output:
  output.write('### VPN CHECKS WERE PERFORMED AT: ' + str(timedate) + ' ###\n')
  output.write('### show running-config | include ' + str(ip) + ' ###\n')
  output.write(running_conf)
  output.write('\n\n### show running-config | include ' + str(CryptoMap[0]) + ' ###\n')
  output.write(config_map)
  output.write('\n\n### show running-config access-list | include ' + str(ipsec[0]) + ' ###\n')
  output.write(access_list)
  output.write('\n\n### show nat ' + str(customer_IP) + ' detail ###\n')
  output.write(nat_ip)
  output.write('\n\n### VPN status BEFORE reset ## show vpn-sessiondb detail l2l filter name ' + str(ip) + ' ###\n')
  output.write(vpnstatus)
  if vpnStatAftrRst != '':
    output.write('\n\n### VPN status AFTER reset ## show vpn-sessiondb detail l2l filter name ' + str(ip) + ' ###\n')
    output.write(vpnStatAftrRst)

print('To view all the logs, use command: more ./Checks_for_VPN_' + ipsec[0] + '_on_FW_' + fw + '.txt')
