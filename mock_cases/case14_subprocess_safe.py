import subprocess

def run_tool(filename):
    return subprocess.run(["cat", filename], check=True, capture_output=True, text=True)
