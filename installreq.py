import os
import subprocess
import json
import time
import sys

current_directory = os.getcwd()
requirements_path = os.path.join(current_directory, 'requirements.txt')

if not os.path.exists(requirements_path):
    print("requirements.txt file not found. The application will close in 5 seconds.")
    time.sleep(5)
    sys.exit()

create_environment = input("Do you want to create a virtual environment? (y/n): ")

if create_environment.lower() == 'y':
    environment_name = "venv." + os.path.basename(current_directory)
    environment_path = os.path.join(current_directory, environment_name)

    if not os.path.exists(environment_path):
        subprocess.check_call(['python', '-m', 'venv', environment_path])

    activate_path = os.path.join(environment_path, 'Scripts' if os.name == 'nt' else 'bin', 'activate')
    subprocess.check_call(activate_path, shell=True)

with open(requirements_path, 'r') as requirements_file:
    requirements_lines = requirements_file.readlines()
    dependencies = [line.strip() for line in requirements_lines]

print("The following dependencies will be installed:")
for dependency in dependencies:
    try:
        result = subprocess.check_output(['pip', 'show', dependency])
        dependency_info = json.loads(result.decode('utf-8'))
        summary = dependency_info['summary']
        if not summary:
            summary = dependency
    except:
        summary = dependency
    print(f"[+] {dependency}: {summary}")

response = input("Do you want to install the dependencies? (y/n): ")
if response.lower() == 'y':
    with subprocess.Popen(['pip', 'install', '-r', requirements_path], stdout=subprocess.PIPE, universal_newlines=True) as process:
        for line in process.stdout:
            print(line, end='')
    print("Installation completed.")
else:
    print("Installation canceled by the user.")

terminate = input("Do you want to terminate the program? (y/n): ")
if terminate.lower() == 'y':
    sys.exit()
