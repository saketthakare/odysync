import argparse
import ConfigParser
import os
from peer import Client

'''def get_watch_dirs(config):
    watch_dirs = []
    for key, value in config.items('sync.sys'):
        watch_dirs.append(value)
    return watch_dirs'''

def main():
    parser = argparse.ArgumentParser(
        description="""Odysync""",
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        '-destination_ip', help='Specify the ip of destination workstation', required=False)
    parser.add_argument(
        '-destination_user', help='Specify the username of destination workstation', required=False)
    parser.add_argument(
        '-dir', help='Specify the directory to be synced', required=False)

    args = parser.parse_args()
    peer = Client(args.dir, args.destination_ip, args.destination_user)
    peer.activate()

if __name__ == "__main__":
    main()
