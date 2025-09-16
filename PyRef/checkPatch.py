import requests
import re

def parse_patch_data(patch_data):
    """
    Parse the patch data to extract all chunks including code modifications.
    
    :param patch_data: The raw patch text data from the API response.
    :return: A list of full patch blocks.
    """
    matching_patches = []
    
    # Split the patch data by each "@@" chunk to isolate blocks
    chunks = re.split(r"(@@ -\d+,\d+ \+\d+,\d+ @@)", patch_data)
    for i in range(1, len(chunks), 2):
        header = chunks[i]
        content = chunks[i + 1]

        # Append the entire patch block (header + content)
        matching_patches.append(header + content)

    return matching_patches

def get_commit_patch(owner, repo, sha, file_path):
    # Truncate the file path to include only up to ".py"
    if ".py" in file_path:
        file_path = file_path[:file_path.index(".py") + 3]

    url = f"https://github.com/{owner}/{repo}/commit/{sha}.diff?path={file_path}"
    print(f"Fetching URL: {url}")
    response = requests.get(url)

    if response.status_code == 200:
        patch_data = response.text
        matching_patches = parse_patch_data(patch_data)
        
        if matching_patches:
            print(f"\nPatch information for {file_path} in commit {sha}:\n")
            for patch in matching_patches:
                print(patch)
        else:
            print("No patch information found.")
    else:
        print(f"Failed to retrieve patch. HTTP Status Code: {response.status_code}")
        if response.status_code == 404:
            print("File not found or commit does not exist.")
        elif response.status_code == 403:
            print("Rate limit exceeded or access forbidden.")
        else:
            print("An unknown error occurred.")

if __name__ == "__main__":
    owner = "iperov"        # Replace with the desired GitHub username
    repo = "DeepFaceLive"    # Replace with the desired GitHub repository name
    sha = "ae8a1e0ff4b13e6e6a0155e346864805b2ca81dd"  # Replace with the commit SHA
    file_path = "xlib/face/FLandmarks2D.py"  # Replace with the file path

    get_commit_patch(owner, repo, sha, file_path)

