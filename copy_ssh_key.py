import subprocess
import sys
import ConfigParser
import os.path
import argparse

my_file = "sync.cfg"
if os.path.exists(my_file):
    if raw_input("Config File exists. do you still want to create new one (y/n) :") == "y":
        Config = ConfigParser.ConfigParser()
        cfgfile = open("sync.cfg",'wb+')
        Config.add_section('dirs')
        print("Setting up config file")

        number_of_workstations = int(raw_input("How many workstation you want to add : "))
        ip = []
        user =[]
        count = 0
        print("Enter username & ip")
        while count < number_of_workstations :
            ip.append(raw_input("IP : "))
            user.append(raw_input("USER : "))
            count = count + 1
        for x in range(number_of_workstations):
            Config.set('dirs', user[x], user[x]+"@"+ip[x])

        Config.write(cfgfile)
        cfgfile.close()
    else:
        Config = ConfigParser.ConfigParser()
        Config.read("sync.cfg")

        number_of_workstations = 0
        ip = []
        user =[]
        for key, value in Config.items('dirs'):
            user.append(key)
            ip.append(value)
            number_of_workstations += 1

else:
    Config = ConfigParser.ConfigParser()
    cfgfile = open("sync.cfg",'wb+')
    Config.add_section('dirs')
    print("Setting up config file")

    number_of_workstations = int(raw_input("How many workstation you want to add : "))
    ip = []
    user =[]
    count = 0
    print("Enter username & ip")
    while count < number_of_workstations :
        ip.append(raw_input("IP : "))
        user.append(raw_input("USER : "))
        count = count + 1
    for x in range(number_of_workstations):
        Config.set('dirs', user[x], user[x]+"@"+ip[x])

    Config.write(cfgfile)
    cfgfile.close()



raw_input("Press Enter to start")

for x in range(number_of_workstations):
    COMMAND = "ssh-copy-id -i $HOME/.ssh/id_dsa.pub "+ip[x]
    #ssh = subprocess.Popen([COMMAND],shell=True)
    print COMMAND
