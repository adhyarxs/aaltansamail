import subprocess
import os
import sys
import time

def clearTerm():
    return subprocess.call('cls' if os.name=='nt' else 'clear',shell=True)

def animText(text):
    for a in text:
        print(a,end="",flush=True)
        time.sleep(0.1)
