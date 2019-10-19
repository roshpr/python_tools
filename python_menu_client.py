#!/usr/bin/env python2.7
import os
import subprocess
 
header = "\
_________   _________________           .__  .__ \n\
\_   ___ \ /   _____/\_____  \     ____ |  | |__|\n\
/    \  \/ \_____  \  /   |   \  _/ ___\|  | |  |\n\
\     \____/        \/    |    \ \  \___|  |_|  |\n\
 \______  /_______  /\_______  /  \___  >____/__|\n\
        \/        \/         \/       \/         \n"
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
    try:
        if output:
            output = subprocess.check_output(command, shell=shell, stderr=subprocess.STDOUT, **kwargs)
            return (True, 0, output)
        else:
            retcode = subprocess.call(command, shell=shell, stderr=subprocess.STDOUT, **kwargs)
            return (True, retcode, None)

    except Exception as ex:
        print 'Exception {}'.format(ex)
        if retry_sudo and 'sudo' not in command and ( "Permission denied" in ex.output or "only root can do that" in ex.output):
            if type(command) is list:
                sudo_cmd = ['sudo'] + command
            else:
                sudo_cmd = 'sudo ' + command
            return run_command(sudo_cmd, output, shell=shell, ignore=ignore, retry_sudo=False, **kwargs)

def print_response(resp):
    print colorize("[" + str(resp) + "] ", 'pink')

def set_maintenance_time():
    time = raw_input("Enter PST UTC time: ")
    run_command('kubectl -n infra exec -it etcd-etcd-0 -- bash -c \"etcdctl set /csp/infra/maintenance/time {}\"'.format(time), ignore=False, output=True)
    resp = run_command('kubectl -n infra exec -it etcd-etcd-0 -- bash -c \"etcdctl get /csp/infra/maintenance/time\"', ignore=False, output=True)
    print 'Response: {}'.format(resp)
    raw_input("Press [Enter] to continue...")
 
def enable_maintenance_banner():
    run_command('kubectl -n infra exec -it etcd-etcd-0 -- bash -c \"etcdctl set /csp/infra/maintenance/enable {}\"'.format('true'), ignore=False, output=True)
    resp = run_command('kubectl -n infra exec -it etcd-etcd-0 -- bash -c \"etcdctl get /csp/infra/maintenance/enable\"', ignore=False, output=True)
    print 'Response: {}'.format(resp)
    raw_input("Press [Enter] to continue...")
 
def disable_maintenance_banner():
    run_command('kubectl -n infra exec -it etcd-etcd-0 -- bash -c \"etcdctl set /csp/infra/maintenance/enable {}\"'.format('false'), ignore=False, output=True)
    resp = run_command('kubectl -n infra exec -it etcd-etcd-0 -- bash -c \"etcdctl get /csp/infra/maintenance/enable\"', ignore=False, output=True)
    print 'Response: {}'.format(resp)
    raw_input("Press [Enter] to continue...")

def show_maintenance_values():
    resp = run_command('kubectl -n infra exec -it etcd-etcd-0 -- bash -c \"etcdctl get /csp/infra/maintenance/time\"', ignore=False, output=True)
    print_response('Time: {}'.format(resp))
    resp = run_command('kubectl -n infra exec -it etcd-etcd-0 -- bash -c \"etcdctl get /csp/infra/maintenance/enable\"', ignore=False, output=True)
    print_response('Enable: {}'.format(resp))
    raw_input("Press [Enter] to continue...")

def set_maintenance():
    maintenance_menu_items = [
      { "Set time": set_maintenance_time },
      { "Enable banner": enable_maintenance_banner },
      { "Disable banner": disable_maintenance_banner },
      { "Show settings": show_maintenance_values },
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
        print colorize(header, 'pink')
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
