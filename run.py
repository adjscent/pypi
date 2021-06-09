"""
A simple offline downloader/installer for pypi packages.
Assumes all the whl files are in the current directory 
"""
import subprocess
from pathlib import Path

package_dir = Path(__file__).parent.absolute()
folder = package_dir.joinpath("local_wheels")

def run_command_and_poll(command):
    p = subprocess.Popen(command,
                         shell=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    return iter(p.stdout.readline, b'')


def run_command(command):
    return subprocess.run(command, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE,
                   check=False).stdout.decode('utf-8').strip()


def run_install(package_name):
    return run_command_and_poll(
        "pip3 install --no-index --find-links {} {}".format(folder, package_name))


def run_download(package_name):
    return run_command_and_poll("pip3 download -d {} {}".format(folder, package_name))


def get_input():
    return input().strip()


def main():
    folder.mkdir(parents=True, exist_ok=True)
    while True:
        print(
            """
What do you want to do?
1. Install
2. Download
"""
        )
        answer = get_input()
        if answer in ["1", "2"]:
            install = answer == "1"
            print("""What package or requirements.txt""")
            answer = get_input()
            package = "-r {}".format(answer) if ".txt" in answer else answer
            if install:
                print("Running install for {}".format(package))
                for i in run_install(package):
                    print(i)
            else:
                print("Running download for {}".format(package))
                for i in run_download(package):
                    print(i)
        else:
            print("Unknown option")


if __name__ == "__main__":
    main()
