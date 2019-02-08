import argparse
import ConfigParser
import os
from master_peer import Client

def get_watch_dirs(config):
    watch_dirs = []
    for key, value in config.items('dirs'):
        watch_dirs.append(value)
    return watch_dirs

def main():
    parser = argparse.ArgumentParser(
        description="""Odysync""",
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument(
        '-dir', help='Specify the  directory to be synced', required=True)
    parser.add_argument(
        '-config', help='Specify the config file', required=True)

    args = parser.parse_args()
    config = ConfigParser.ConfigParser()
    config.read(args.config)
    peer = Client(args.dir, get_watch_dirs(config))
    peer.activate()

if __name__ == "__main__":
    main()
