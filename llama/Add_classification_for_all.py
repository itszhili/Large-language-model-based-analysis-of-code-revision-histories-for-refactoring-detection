# Copyright (c) Meta Platforms, Inc. and affiliates.
# This software may be used and distributed according to the terms of the Llama 2 Community License Agreement.

from typing import List, Optional
import csv
import fire
from llama import Llama, Dialog
import json
import os
import textwrap

# Hardcoded paths for the CSV file and JSON directory
csv_file_path = '/mimer/NOBACKUP/groups/2023-llm-refactoring/PyRef/Applications_less_commits_175.csv'
json_file_directory = '/mimer/NOBACKUP/groups/2023-llm-refactoring/PyRef'

def format_classification_text(text, width=100):
    """
    Splits the classification text into a list of strings at a specified width.
    
    Args:
        text (str): The text to format.
        width (int): The desired width before breaking into a new list item.
        
    Returns:
        List[str]: The formatted text as a list of lines.
    """
    return textwrap.wrap(text, width)

def process_project_json(generator, project_json_path, max_gen_len, temperature, top_p):
    with open(project_json_path, 'r') as file:
        refactoring_data = json.load(file)

    dialogs = []
    for block in refactoring_data:
        # print(f"Processing block in file: {project_json_path}")
        # print(f"Available keys: {list(block.keys())}")
        
        # Create a string representation of each key-value pair
        key_value_pairs = [f"{key}: {block[key]}" for key in block]
        # Join all key-value pairs into a single string with a comma and space separator
        content = ", ".join(key_value_pairs)
        dialog = [{"role": "user", "content": f"Is this a machine learning specific software refactoring or a general software refactoring? {content}"}]
        dialogs.append(dialog)
   
    results = generator.chat_completion(
        dialogs,  # type: ignore
        max_gen_len=max_gen_len, 
        temperature=temperature,
        top_p=top_p,
    )

    for block, result in zip(refactoring_data, results):
        lines_of_classification = format_classification_text(result['generation']['content'], width=100)
        block['Classification'] = lines_of_classification

    # Generate a new file name for the updated data
    new_file_name = os.path.basename(project_json_path).replace(".json", "_with_classification.json")
    new_file_path = os.path.join(json_file_directory, new_file_name)

    # Save the updated data to the new file
    with open(new_file_path, 'w', encoding='utf-8') as file:
        json.dump(refactoring_data, file, ensure_ascii=False, indent=4)

def main(
    ckpt_dir: str,
    tokenizer_path: str,
    temperature: float = 0.6,
    top_p: float = 0.9,
    max_seq_len: int = 512,
    max_batch_size: int = 8,
    max_gen_len: Optional[int] = None,
):
    generator = Llama.build(
        ckpt_dir=ckpt_dir,
        tokenizer_path=tokenizer_path,
        max_seq_len=max_seq_len,
        max_batch_size=max_batch_size,
    )

    with open(csv_file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        #next(reader)  # Skip the header row if present
        for row in reader:
            project_name = row[1].split('/')[-1]  # Extract project name from owner/repo format
            json_file_name = f"{project_name}_data.json"
            json_file_path = os.path.join(json_file_directory, json_file_name)

            if os.path.exists(json_file_path):
                print(f"Processing {json_file_name}...")
                process_project_json(generator, json_file_path, max_gen_len, temperature, top_p)
            else:
                print(f"File {json_file_name} not found.")

if __name__ == "__main__":
    fire.Fire(main)
