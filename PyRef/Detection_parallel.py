import csv
import os
import subprocess
from concurrent.futures import ProcessPoolExecutor

# Path to the CSV file
csv_file_path = '/mimer/NOBACKUP/groups/2023-llm-refactoring/PyRef/Applications_less_commits_175.csv'
repo_base_path = '/mimer/NOBACKUP/groups/2023-llm-refactoring/PyRef/Repos'
data_json_path = '/mimer/NOBACKUP/groups/2023-llm-refactoring/PyRef'  

def repo_exists(repo_path):
    return os.path.isdir(repo_path)

def get_repo_name(full_name):
    return full_name.split('/')[-1] 

def json_exists(repo_name):
    json_file = f'{data_json_path}/{repo_name}_data.json'
    return os.path.isfile(json_file)


def detect_refactorings(repo_name):
    command = f'python main.py getrefs -r "Repos/{repo_name}"'
    subprocess.run(command, shell=True)

def process_repo(row):
    serial_number, full_repo_name = row
    repo_name = get_repo_name(full_repo_name)
    repo_path = f'{repo_base_path}/{repo_name}'

    if repo_exists(repo_path):
        if not json_exists(repo_name):
            print(f"Detecting for {serial_number}, Repo Name: {repo_name}")
            detect_refactorings(repo_name)
            
            if json_exists(repo_name):
                print(f"Completed detection for {serial_number}, Repo Name: {repo_name}")
            else:
                print(f"Error in detection for {serial_number}, Repo Name: {repo_name}")
        else:
            print(f"Skipping detection, JSON file already exists: Serial Number: {serial_number}, Repo Name: {repo_name}")
    else:
        print(f"Repo not found: Serial Number: {serial_number}, Repo Name: {repo_name}")

# Read the CSV and process each repo in parallel
with open(csv_file_path, newline='') as csvfile:
    reader = csv.reader(csvfile)
    # next(reader)  
    rows = list(reader)

# Using ProcessPoolExecutor to run tasks in parallel
with ProcessPoolExecutor() as executor:
    # Submit each repo for processing
    futures = [executor.submit(process_repo, row) for row in rows]

    # Wait for all futures to complete
    for future in futures:
        future.result()