import subprocess
import sys
import ConfigParser
Config = ConfigParser.ConfigParser()
cfgfile = open("sync.cfg",'wb+')
Config.add_section('dirs')



print("Setting up config file")
home_ip = raw_input("Enter your home IP : ")
home_user = raw_input("Enter your home username")

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


raw_input("Press Enter to start master")

commd = "python /home/"+home_user+"/odysync/master_init.py -dir /home/"+home_user+"/sync/ -config /home/"+home_user+"/odysync/sync.cfg &"
print commd
master = subprocess.Popen([commd],shell=True)
#raw_input("Press Enter to start other workstations")

for x in range(number_of_workstations):
    HOST=user[x]+"@"+ip[x]
    COMMAND = "ssh "+HOST+" python /home/"+user[x]+"/odysync/init.py -dir /home/"+user[x]+"/sync -destination_ip "+home_ip+" -destination_user "+home_user+" &"
    ssh = subprocess.Popen([COMMAND],shell=True)
    print COMMAND
