from pyinotify import WatchManager, ProcessEvent
import pyinotify
import subprocess
import time
import threading
import os

from sync_loop import sync_all
from persistence import FileData, FilesPersistentSet

class PTmp(ProcessEvent):
    def __init__(self, mfiles, rfiles, pulledfiles):
        self.mfiles = mfiles
        self.rfiles = rfiles
        self.pulled_files = pulledfiles

    def process_IN_CREATE(self, event):
        filename = os.path.join(event.path, event.name)
        if not self.pulled_files.__contains__(filename):
            self.mfiles.add(filename, time.time())
        else:
            pass
            self.pulled_files.remove(filename)

    def process_IN_DELETE(self, event):
        filename = os.path.join(event.path, event.name)
        self.rfiles.add(filename)
        try:
            self.mfiles.remove(filename)
        except KeyError:
            pass

    def process_IN_MODIFY(self, event):
        filename = os.path.join(event.path, event.name)
        if not self.pulled_files.__contains__(filename):
            self.mfiles.add(filename, time.time())
        else:
            self.pulled_files.remove(filename)

class Client():
    def __init__(self, dir, destination_ip, destination_user):
        self.dir = dir
        self.destination_ip = destination_ip
        self.destination_user = destination_user
        self.mfiles = FilesPersistentSet(pkl_filename = 'client.pkl')
        self.rfiles = set()
        self.pulled_files = set()

    def push_pull_file(self):
        push_status = sync_all(self.dir, self.destination_ip, self.destination_user)
        return push_status

    def find_modified(self):
        dirwalk = os.walk(self.dir)
        for tuple in dirwalk:
            dirname, dirnames, filenames = tuple
            break
        for filename in filenames:
            file_path = os.path.join(dirname,filename)
            print "checked file if modified before client was running: %s" % file_path
            mtime = os.path.getmtime(file_path)
            if mtime > self.mfiles.get_modified_timestamp():
                print "modified before client was running %s", file_path
                self.mfiles.add(file_path, mtime)

    def sync_files(self):
        mfiles = self.mfiles
        while True:
            try:
                time.sleep(10)
                if len(mfiles.list())>0:
                    self.push_pull_file()
                for filedata in mfiles.list():
                    filename = filedata.name
                    mfiles.remove(filename)
                self.mfiles.update_modified_timestamp()
            except KeyboardInterrupt:
                break

    def watch_files(self):
        wm = WatchManager()
        mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE | pyinotify.IN_MODIFY
        notifier = pyinotify.Notifier(wm, PTmp(self.mfiles, self.rfiles, self.pulled_files))
        wm.add_watch(os.path.expanduser(self.dir), mask, rec=False, auto_add=True)
        while True:
            try:
                time.sleep(5)
                notifier.process_events()
                if notifier.check_events():
                    notifier.read_events()
            except KeyboardInterrupt:
                notifier.stop()
                break

    def start_watch_thread(self):
        watch_thread = threading.Thread(target=self.watch_files)
        watch_thread.start()

    def start_sync_thread(self):
        sync_thread = threading.Thread(target=self.sync_files)
        sync_thread.start()

    def activate(self):
        self.start_sync_thread()
        self.start_watch_thread()
        self.find_modified()
