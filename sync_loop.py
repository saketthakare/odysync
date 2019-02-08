import subprocess

def sync_all(source,destination_ip,destination_user):
    destination = "ssh://"+destination_user+"@"+destination_ip+"//home/"+destination_user+"/sync"
    proc = subprocess.Popen(["unison", "-batch",source,destination])
    push_status = proc.wait()
    return push_status
