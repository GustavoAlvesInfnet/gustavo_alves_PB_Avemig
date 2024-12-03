import subprocess

def run_streamlit():
    subprocess.Popen(["start", "streamlit", "run", r".\main\streamlitAPP.py"], shell=True)

def run_uvicorn():
    subprocess.Popen(["start", "uvicorn", "main.API:app", "--reload"], shell=True)

if __name__ == "__main__":
    run_streamlit()
    run_uvicorn()