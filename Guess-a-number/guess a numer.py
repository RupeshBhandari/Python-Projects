import random
from termcolor import colored
import time
import sys


flag = True
while flag == True:
    random_number = random.randint(1, 10)
    user_input = int(input(colored("\n       Enter a number from 1 to 10>>   ",'blue')))
    if user_input == random_number:
        right_string = "\n               ( ͡° ͜ʖ ͡°)                Yay, you've guessed it correctly!"
        for i in right_string:
            print(colored(f'{i}', 'green'), end='')
            sys.stdout.flush()
            time.sleep(0.1)
        print('')
        play_again = input(colored("\n       Do you want to try again?       ", 'blue'))
    else:
        wrong_string = f"\n             ¯\_( ͡° ͜ʖ ͡°)_/¯            Sorry, your guess is wrong! The number was: {random_number}"
        for i in wrong_string:
            print(colored(f'{i}', 'red'), end='')
            sys.stdout.flush()
            time.sleep(0.1)
        print('')
        play_again = input(colored("\n       Do you want to try again?       ", 'blue'))
    if play_again.lower() == 'y' or play_again.lower() == 'yes':
        flag = True
    else:
        flag = False
        
        
