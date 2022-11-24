import os
import miner

log = ""
for file in os.listdir(os.getcwd()):
    if "dumpsys_meminfo" in file:
        log = open(file, "r", errors="ignore").readlines()
        break




