import requests
from termcolor import colored
import sys
import time


ownname = input(colored("\n         Enter your first name:> ", 'blue'))

partnername = input(colored("\n         Enter your partner/lover/crush name:> ", 'blue'))

url = "https://love-calculator.p.rapidapi.com/getPercentage"
querystring = {"fname":f"{ownname}","sname":f"{partnername}"}
headers = {
            'x-rapidapi-key': "(Enter your API Key)",
            'x-rapidapi-host': "(Enter your API Host)"
            }
response = requests.request("GET", url, headers=headers, params=querystring)
response = response.json()
percentage = f"\n         Your compatibility percentage is {response['percentage']}%.\n"

suggestion = f"\n         Suggestion: {response['result']}\n\n"
for i in percentage:
    print(colored(f"{i}", 'magenta'), end='')
    sys.stdout.flush()
    time.sleep(0.1)

if int(response['percentage']) > 50: 
    color = 'green' 
else:
    color = 'red'

for j in suggestion:
    print(colored(f"{j}", f"{color}"), end ='')
    sys.stdout.flush()
    time.sleep(0.1)