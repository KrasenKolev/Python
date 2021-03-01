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


import random
from os import system

rules = """##                                              ##
## RULES:                                       ##
## Highest number is doing 1st thing            ##
## Middle number is doing 2nd thing             ##
## lowest number is doing 3rd thing             ##
## positions are evaluated from left to right   ##
##                                              ##"""

system('clear')
print(50 * '#')
print(rules)
print(50 * '#')

user1 = input('Please provide position for user 1: \n')
user2 = input('Please provide position for user 2: \n')
user3 = input('Please provide position for user 3: \n')

UsersPositions = {}
rand_lst = []

def verifyInput():
    if int(user1) not in range(1, 4):
      print('\nincorrect position has been provided for user 1. Please run the script again! \n')
      exit()
    elif int(user2) not in range(1, 4):
      print('\nincorrect position has been provided for user 2. Please run the script again! \n')
      exit()
    elif int(user3) not in range(1, 4):
      print('\nincorrect position has been provided for user 3. Please run the script again! \n')
      exit()

def user1Position():
  if user1 == '1':
      UsersPositions['1'] = 'user 1'
  elif user1 == '2':
      UsersPositions['2'] = 'user 1'
  elif user1 == '3':
      UsersPositions['3'] = 'user 1'

def user2Position():
  if user2 == '1':
      UsersPositions['1'] = 'user 2'
  elif user2 == '2':
      UsersPositions['2'] = 'user 2'
  elif user2 == '3':
      UsersPositions['3'] = 'user 2'

def user3Position():
  if user3 == '1':
      UsersPositions['1'] = 'user 3'
  elif user3 == '2':
      UsersPositions['2'] = 'user 3'
  elif user3 == '3':
      UsersPositions['3'] = 'user 3'

def rand_nums():
  rand_lst.append(random.randint(1, 9))
  rand_lst.append(random.randint(1, 9))
  rand_lst.append(random.randint(1, 9))

def rand_nums_check():
    while rand_lst[0] == rand_lst[1] or rand_lst[0] == rand_lst[2] or rand_lst[1] == rand_lst[2]:
      rand_lst.clear()
      rand_nums()

def SR():
  if rand_lst[0] > rand_lst[1] and rand_lst[0] > rand_lst[2]:
      print(50 * '=', '\n')
      print('{user} will be doing 1st thing \n'.format(user = UsersPositions['1']))
  elif rand_lst[1] > rand_lst[0] and rand_lst[1] > rand_lst[2]:
      print(50 * '=', '\n')
      print('{} will be doing 1st thing \n'.format(UsersPositions['2']))
  elif rand_lst[2] > rand_lst[0] and rand_lst[2] > rand_lst[1]:
      print(50 * '=', '\n')
      print('{} will be doing 1st thing \n'.format(UsersPositions['3']))

def HO():
  if rand_lst[0] < rand_lst[1] and rand_lst[0] < rand_lst[2]:
      print('{user} will be doing 2nd thing \n'.format(user = UsersPositions['1']))
  elif rand_lst[1] < rand_lst[0] and rand_lst[1] < rand_lst[2]:
      print('{} will be doing 2nd thing \n'.format(UsersPositions['2']))
  elif rand_lst[2] < rand_lst[0] and rand_lst[2] < rand_lst[1]:
      print('{} will be doing 2nd thing \n'.format(UsersPositions['3']))

def eks():
  if rand_lst[0] < rand_lst[1] and rand_lst[0] > rand_lst[2]:
      print('{user} will be doing 3rd thing \n'.format(user = UsersPositions['1']))
  elif rand_lst[1] < rand_lst[0] and rand_lst[1] > rand_lst[2]:
      print('{} will be doing 3rd thing \n'.format(UsersPositions['2']))
  elif rand_lst[2] < rand_lst[0] and rand_lst[2] > rand_lst[1]:
      print('{} will be doing 3rd thing \n'.format(UsersPositions['3']))
  if rand_lst[0] > rand_lst[1] and rand_lst[0] < rand_lst[2]:
      print('{user} will be doing 3rd thing \n'.format(user = UsersPositions['1']))
  elif rand_lst[1] > rand_lst[0] and rand_lst[1] < rand_lst[2]:
      print('{} will be doing 3rd thing \n'.format(UsersPositions['2']))
  elif rand_lst[2] > rand_lst[0] and rand_lst[2] < rand_lst[1]:
      print('{} will be doing 3rd thing \n'.format(UsersPositions['3']))

def main():
    verifyInput()
    user1Position()
    user2Position()
    user3Position()
    rand_nums()
    rand_nums_check()
    SR()
    HO()
    eks()

if __name__ == '__main__':
  main()

print('\nRandomly generated numbers were: ', rand_lst, '\n')
