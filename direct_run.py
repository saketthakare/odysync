import subprocess
import sys
import ConfigParser
import os.path
import argparse


def main():
    parser = argparse.ArgumentParser(
        description="""Odysync""",
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument(
        '-home_ip', help='Specify the ip of home', required=True)
    parser.add_argument(
        '-home_user', help='Specify the home user', required=True)

    args = parser.parse_args()
    Config = ConfigParser.ConfigParser()
    Config.read("sync.cfg")

    number_of_workstations = 0
    ip = []
    user =[]
    for key, value in Config.items('dirs'):
        user.append(key)
        ip.append(value.split('@')[-1])
        number_of_workstations += 1
    home_ip = args.home_ip
    home_user = args.home_user

    commd = "python /home/"+home_user+"/odysync/master_init.py -dir /home/"+home_user+"/sync/ -config /home/"+home_user+"/odysync/sync.cfg &"
    print commd
    master = subprocess.Popen([commd],shell=True)
    #raw_input("Press Enter to start other workstations")

    for x in range(number_of_workstations):
        HOST=user[x]+"@"+ip[x]
        COMMAND = "ssh "+HOST+" python /home/"+user[x]+"/odysync/init.py -dir /home/"+user[x]+"/sync -destination_ip "+home_ip+" -destination_user "+home_user+" &"
        ssh = subprocess.Popen([COMMAND],shell=True)
        print COMMAND


if __name__ == "__main__":
    main()
