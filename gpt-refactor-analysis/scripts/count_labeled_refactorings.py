import json

with open('DeepFaceLive_data_with_classification.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

category_count = sum(1 for item in data if 'Category2' in item)

print(f'The number of labeled refactoring is: {category_count}')
