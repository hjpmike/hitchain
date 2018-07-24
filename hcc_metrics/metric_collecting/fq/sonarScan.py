import os
import subprocess

def runSonarScanner(repo_path):
    sonar_scanner_command = 'sonar-scanner'
    if not os.path.isdir(repo_path):
        print("Invalid path!")
    else:
        os.chdir(repo_path)
        print('Sonar Scanner Begin.')
        proc = subprocess.call(sonar_scanner_command, shell=True)
        # proc = subprocess.Popen(sonar_scanner_command, shell=True, stdout=subprocess.PIPE)
        # proc.wait()
        # logs = proc.stdout.read()
        print('Sonar Scanner End.')

