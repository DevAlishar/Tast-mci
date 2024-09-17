import subprocess
from watchgod import run_process

def main():
    command = ["uvicorn", "main:app", "--reload"]
    run_process("app", command)

if __name__ == "__main__":
    main()
