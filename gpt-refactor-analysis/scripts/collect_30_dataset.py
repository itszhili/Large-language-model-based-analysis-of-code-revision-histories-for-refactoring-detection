import os
import random
import json
import pandas as pd

csv_file = 'Applications_less_commits_175.csv'  
df = pd.read_csv(csv_file, header=None, names=['sequence', 'project_file'])

def generate_json_filename(project_file):
    filename = project_file.split('/')[-1]  
    return f'{filename}_data.json'


eligible_files = []
for idx, row in df.iterrows():
    json_file = generate_json_filename(row['project_file'])
    if os.path.exists(json_file):  
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if len(data) > 5: 
                eligible_files.append(json_file)

selected_files = random.sample(eligible_files, 6)

collected_blocks = []
for file in selected_files:
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        selected_blocks = random.sample(data, 5)
        collected_blocks.extend(selected_blocks)

output_file = '30_dataset.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(collected_blocks, f, ensure_ascii=False, indent=4)

print(f"30 blocks collected and saved to {output_file}")
