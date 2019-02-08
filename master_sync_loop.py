import subprocess

def before(value):
    pos_a = value.find("@")
    if pos_a == -1: return ""
    return value[0:pos_a]

def sync_dir(source,destination):
    user = before(destination)
    destination = "ssh://"+destination+"//home/"+user+"/sync"
    proc = subprocess.Popen(["unison", "-batch",source,destination])
    push_status = proc.wait()
    return push_status
def sync_all(dir,watch_dirs):
    for each_dir in watch_dirs:
        sync_dir(dir,each_dir)
    return 1
