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


'''
This script will: 
1. Prompt the user for IP addresses as input.
2. Check if the provided IP addresses are valid (both private and public IPs can be used).
3. Run 'traceroute' to each IP address and it will print the result on the screen.
'''

#!/usr/bin/env python

__version__ = 1.0

import sys
import os
import time
import re

print("Enter/Paste the destination IP addresses, hit Enter and Ctrl+D to run the script.")

def input(prompt):
    print(prompt, end='', file=sys.stderr)
    return sys.stdin.readline()

Input = [line for line in sys.stdin]

### REGEX WHICH IS VALIDATING THE PROVIDED IPs ##
VALID_IP = [ ]
REGEX = re.compile(r'([0-9]?){3}\.([0-9]*){3}\.([0-9]*){3}\.([0-9]*){3}')

## VALIDATE THE PROVIDED IP ADDRESSES ##
for line in Input:
   IPObj =  re.search(REGEX, line)
   if IPObj:
      VALID_IP.append(IPObj.group()) ## append all the returned IP addresses to a list  ###

## DO TRACE TO EVERY VALID IP ADDRESS ##
for ip in VALID_IP:
   print()
   print('#### starting traceroute to: '+ ip + ' at %s ###' %time.ctime())
   os.system('traceroute ' + ip)


## SCRIPT END
##

