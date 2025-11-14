import json

# Read URLs from the txt file
with open('30url.txt', 'r') as f:
    urls = [line.strip() for line in f if line.strip()]

# Read the json file
with open('30_dataset.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Ensure the number of URLs matches the number of refactoring entries
assert len(urls) == len(data), "The number of URLs does not match the number of refactorings."

# Add each URL to the corresponding refactoring entry
for i, block in enumerate(data):
    block['URL'] = urls[i]

# Write the updated data back to the json file
with open('30_dataset.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("URLs have been successfully added to each refactoring entry.")

