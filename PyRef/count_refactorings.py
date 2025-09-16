import csv
import json
import os

def count_refactorings_in_json(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return len(data)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return 0
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file: {file_path}")
        return 0

def main(csv_file_path):
    total_refactorings = 0

    with open(csv_file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            owner_repo = row[1]
            repo_name = owner_repo.split('/')[-1]  
            json_file_name = f"{repo_name}_data.json"
            
            refactoring_count = count_refactorings_in_json(json_file_name)
            total_refactorings += refactoring_count

    print(f"Total refactorings across all repositories: {total_refactorings}")

if __name__ == "__main__":
    csv_file_path = 'Applications_less_commits_175.csv' 
    main(csv_file_path)
