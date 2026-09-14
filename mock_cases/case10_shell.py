import subprocess

def run_user_input(command):
    return subprocess.run(command, shell=True, capture_output=True, text=True)
