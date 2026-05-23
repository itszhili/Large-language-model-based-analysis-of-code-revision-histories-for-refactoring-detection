import csv
import json;
import os

# Input CSV file
input_csv = "Applications_less_commits_175.csv"

# Output CSV file
output_csv = "filtered_repos_100_200.csv"

results = []  # Store matched results here

# Read the input CSV file
with open(input_csv, "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    for row in reader:
        if len(row) < 2:
            continue

        index = row[0].strip()
        repo = row[1].strip()  # Example: ageitgey/face_recognition
        repo_name = repo.split("/")[-1]  # Extract repo name such as "face_recognition"

        # JSON filename pattern (modify here if your naming rule differs)
        json_filename = f"{repo_name}_data.json"

        if not os.path.exists(json_filename):
            print(f"[Warning] JSON file not found: {json_filename}")
            continue

        # Read JSON file
        with open(json_filename, "r", encoding="utf-8") as jf:
            try:
                data = json.load(jf)
            except json.JSONDecodeError:
                print(f"[Error] Invalid JSON format: {json_filename}")
                continue

        count = len(data)

        # Keep only projects with 100–200 refactoring entries
        if 100 <= count <= 10000000:
            results.append([index, repo, json_filename])

# Write results into the output CSV file
with open(output_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Index", "Repo Name", "JSON Filename"])
    writer.writerows(results)

# Print summary
print("Number of matched projects:", len(results))
print("Output file generated:", output_csv)

# Print each matched entry
for i, (index, repo, json_file) in enumerate(results, 1):
    print(i, index, repo, json_file)
