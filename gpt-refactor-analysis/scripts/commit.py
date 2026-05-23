import requests
import base64

# Configuration for the request
owner = "xinshuoweng"
repo = "AB3DMOT"
path = "main.py"
sha = "090fdbea4409a871c17368191402e7de6f25e127"

# Construct the API URL
url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}?ref={sha}"

# Make the request
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    content_info = response.json()
    # Decode the Base64 encoded content
    file_content = base64.b64decode(content_info['content']).decode('utf-8')
else:
    print("Failed to retrieve the file content")

print(file_content)
