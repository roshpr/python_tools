#!/usr/bin/env python2.7
import os
import subprocess
 
colors = {
        'blue': '\033[94m',
        'pink': '\033[95m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        }
 
def colorize(string, color):
    if not color in colors: return string
    return colors[color] + string + '\033[0m'

def run_command(command, output=True, shell=True, ignore=False, retry_sudo=False,  **kwargs):
    return "Success"

def print_response(resp):
    print colorize("[" + str(resp) + "] ", 'pink')

def enable_banner():
    run_command('etcdctl set /enable {}'.format('true'), ignore=False, output=True)
    resp = run_command('etcdctl get /enable', ignore=False, output=True)
    print 'Response: {}'.format(resp)
    raw_input("Press [Enter] to continue...")
 

def show_values():
    resp = run_command('etcdctl get /time', ignore=False, output=True)
    print_response('Time: {}'.format(resp))
    resp = run_command('etcdctl get /enable', ignore=False, output=True)
    print_response('Enable: {}'.format(resp))
    raw_input("Press [Enter] to continue...")

def set_maintenance():
    maintenance_menu_items = [
      { "Enable banner": enable_banner },
      { "Show settings": show_values },
      { "Main menu": main_menu },
    ]
    while True:
        for item in maintenance_menu_items:
            print colorize("[" + str(maintenance_menu_items.index(item)) + "] ", 'yellow') + item.keys()[0]
        choice = raw_input(">> ")
        try:
            if int(choice) < 0 : raise ValueError
            # Call the matching function
            maintenance_menu_items[int(choice)].values()[0]()
        except (ValueError, IndexError):
            pass

menuItems = [
    { "Set maintenance": set_maintenance },
    { "Exit": exit },
]
 
def main_menu():
    while True:
        os.system('clear')
        # Print some badass ascii art header here !
        #print colorize(header, 'pink')
        print colorize('version 0.1\n', 'green')
        for item in menuItems:
            print colorize("[" + str(menuItems.index(item)) + "] ", 'blue') + item.keys()[0]
        choice = raw_input(">> ")
        try:
            if int(choice) < 0 : raise ValueError
            # Call the matching function
            menuItems[int(choice)].values()[0]()
        except (ValueError, IndexError):
            pass
 
def main():
    main_menu()

if __name__ == "__main__":
    main()
