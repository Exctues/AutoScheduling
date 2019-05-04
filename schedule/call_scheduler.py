import subprocess
from subprocess import Popen, PIPE
from sys import platform
import os

def run(path_to_config):
    cwd = os.path.dirname(os.path.abspath(__file__))
    print(cwd)

    if platform == "win32":
        subprocess.call(["cmake", '-GMinGW Makefiles', cwd + "/../scheduler_cpp/"])
        subprocess.call(["mingw32-make"])
        p = Popen(["./automatic-timetable-system.exe", path_to_config], stdout=PIPE, stderr=PIPE)
    else:
        subprocess.call(["cmake", cwd + "/../scheduler_cpp/"])
        subprocess.call(["make"])
        p = Popen(["./automatic-timetable-system", path_to_config], stdout=PIPE, stderr=PIPE)

    output, err = p.communicate()
    if err.decode() == '':
        print(output.decode())
        return output.decode()
