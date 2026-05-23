import requests
import re
import json
import copy

def filter_by_keywords(patch_data, original_keyword, updated_keyword):
    matching_patches = []
    
    chunks = re.split(r"(@@ -\d+,\d+ \+\d+,\d+ @@)", patch_data)
    for i in range(1, len(chunks), 2):
        header = chunks[i]
        content = chunks[i + 1]

        # Split lines of the content to check individual lines
        lines = content.splitlines()
        original_found = False
        updated_found = False

        for line in lines:
            if line.startswith("-") and original_keyword in line:
                original_found = True
            elif line.startswith("+") and updated_keyword in line:
                updated_found = True

            # If both conditions are met, this patch matches the criteria
            if original_found and updated_found:
                matching_patches.append(header + content)
                break  # No need to check further lines in this patch

    return matching_patches

def filter_by_line_range(patches, target_lines):
    filtered_patches = []

    for patch in patches:
        header = patch.splitlines()[0]
        content = "\n".join(patch.splitlines()[1:])

        match = re.match(r"@@ -(\d+),(\d+) \+(\d+),(\d+) @@", header)
        if match:
            original_start = int(match.group(1))
            original_length = int(match.group(2))
            updated_start = int(match.group(3))
            updated_length = int(match.group(4))

            if (original_start <= target_lines["original"] < original_start + original_length and 
                updated_start <= target_lines["updated"] < updated_start + updated_length):
                
                filtered_patches.append(patch)

    return filtered_patches

def get_commit_patch(owner, repo, sha, file_path, target_lines, original_keyword, updated_keyword):
    url = f"https://github.com/{owner}/{repo}/commit/{sha}.diff?path={file_path}"
    print(f"Fetching URL: {url}")
    response = requests.get(url)

    if response.status_code == 200:
        patch_data = response.text
        
        patches_with_keywords = filter_by_keywords(patch_data, original_keyword, updated_keyword)
        
        if target_lines["original"] is None or target_lines["updated"] is None:
            return patches_with_keywords
        
        final_patches = filter_by_line_range(patches_with_keywords, target_lines)
        return final_patches
    elif response.status_code == 404:
        print("File not found or commit does not exist.")
    elif response.status_code == 403:
        print("Access forbidden or rate limit exceeded.")
    else:
        print(f"An unknown error occurred. HTTP Status Code: {response.status_code}")
    
    return []

def process_json_file(json_file_path, output_json_path):
    owner = "iperov"        
    repo = "DeepFaceLive"

    with open(json_file_path, "r") as file:
        data = json.load(file)

    updated_data = copy.deepcopy(data)

    for i, entry in enumerate(updated_data):
        commit = entry.get("Commit")
        
        file_path = entry.get("Location")
        
        if file_path is None:
            file_path = entry.get("New Location", entry.get("Old Location"))

        if file_path and ".py" in file_path:
            file_path = file_path[:file_path.index(".py") + 3]
        
        if file_path is None:
            print(f"Warning: 'Location', 'New Location', and 'Old Location' fields are missing for entry {i}. Skipping this entry.")
            continue
        
        original_line = entry.get("Original Line")
        updated_line = entry.get("Updated Line")
        original_keyword = entry.get("Original")
        updated_keyword = entry.get("Updated")

        target_lines = {
            "original": original_line,
            "updated": updated_line
        }

        print(f"\nProcessing commit {commit} for file {file_path}...\n")
        patches = get_commit_patch(owner, repo, commit, file_path, target_lines, original_keyword, updated_keyword)

        entry["Patch Information"] = patches if patches else []

    with open(output_json_path, "w") as output_file:
        json.dump(updated_data, output_file, indent=4)

    print(f"\nUpdated JSON file with filtered patch information has been saved to: {output_json_path}")

if __name__ == "__main__":
    json_file_path = "DeepFaceLive_data.json"    
    output_json_path = "DeepFaceLive_data2.json"  
    process_json_file(json_file_path, output_json_path)
