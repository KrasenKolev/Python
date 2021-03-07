# Python


## multiTracerouteV2

multiTraceroute script will: 
1. Prompt the user for IP addresses as input.
2. Check if the provided IP addresses are valid (both private and public IPs can be used).
3. Run 'traceroute' to each of the provided IP addresses and it will attach the traceroute results to 'output.txt' file in the present working directory.

## multiTraceroute

multiTraceroute script will: 
1. Prompt the user for IP addresses as input.
2. Check if the provided IP addresses are valid (both private and public IPs can be used).
3. Run 'traceroute' to each of the provided IP addresses and it will print the result on the screen.

## duties

duties is a Python script designed to assign different task to each of 3 users based on randomly generated numbers. 
1. each user has to select digit position (from 1 to 3, evaluated from left to right).
2. the script will generate 3 random digits.
3. based on the position and the random value, the script will assign task to each user. 

  example scenario: let's say user1 selected position 1, user2 selected position 2, user3 selected position 3. Let's say that the randomly generated numbers are [3,   5, 9]. Because user1 selected position 1 and it happens to be the lowest value among the other 2 values, so user1 will get assigned the task bound to the lowest     value. User 2 will get assigned the task bound to the middle value. User3 will get assigned the task bound to the highest value. 
  The tasks are static, however, every user can select any of the possitions (from 1 to 3) and based on the random value every user might get different task           assigned every time the script is run.
  
  NOTES: 
  1. If it happens the some of the randomly generated values to be the same, the script will generate new values untill they are all different. 
  2. If the user provides input different digits than digits from 1 to 3, the script will stop.
