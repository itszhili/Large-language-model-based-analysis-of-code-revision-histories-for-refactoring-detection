import json

# Path to your JSON file
json_file_path = 'ai-art-generator_data.json'

# Load the JSON data from the file
with open(json_file_path, 'r') as file:
    refactoring_data = json.load(file)

# Initialize an empty list to store the formatted content from each block
content_list = []

# Loop through each block in the JSON data
for block in refactoring_data:
    # Format the information from the block into a string
    content = (f"Refactoring Type: {block['Refactoring Type']}, "
               f"Original: {block['Original']}, "
               f"Updated: {block['Updated']}, "
               f"Location: {block['Location']}, "
               f"Description: {block['Description']}, "
               f"Commit: {block['Commit']}")
    # Append the formatted string to the content list
    content_list.append(content)

# Example: Print each content string in the content list
for content in content_list:
    print(content)
