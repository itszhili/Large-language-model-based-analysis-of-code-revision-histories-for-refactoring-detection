# Copyright (c) Meta Platforms, Inc. and affiliates.
# This software may be used and distributed according to the terms of the Llama 2 Community License Agreement.

from typing import List, Optional

import fire

from llama import Llama, Dialog

import json
import os
import torch
import textwrap

# Path to JSON file
json_file_path = '/mimer/NOBACKUP/groups/2023-llm-refactoring/PyRef/face_recognition_data.json'
# output_json_suffix = '_with_fewshot_classification.json'
output_json_suffix = 'Llama_short.json'

# Generate the output file name
base_name = os.path.basename(json_file_path)
name_without_ext = os.path.splitext(base_name)[0]
output_file_name = name_without_ext + output_json_suffix
output_file_path = os.path.join(os.path.dirname(json_file_path), output_file_name)

with open(json_file_path, 'r') as file:
    refactoring_data = json.load(file)

content_list = []

for block in refactoring_data:
    key_value_pairs = [f"{key}: {block[key]}" for key in block]
    content = ", ".join(key_value_pairs)
    content_list.append(content)



# for content in content_list:
#     print(content)

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



# def main(
#     ckpt_dir: str,
#     tokenizer_path: str,
#     temperature: float = 0.6,
#     top_p: float = 0.9,
#     max_seq_len: int = 512,
#     max_batch_size: int = 8,
#     max_gen_len: Optional[int] = None,
# ):
#     """
#     Entry point of the program for generating text using a pretrained model.

#     Args:
#         ckpt_dir (str): The directory containing checkpoint files for the pretrained model.
#         tokenizer_path (str): The path to the tokenizer model used for text encoding/decoding.
#         temperature (float, optional): The temperature value for controlling randomness in generation.
#             Defaults to 0.6.
#         top_p (float, optional): The top-p sampling parameter for controlling diversity in generation.
#             Defaults to 0.9.
#         max_seq_len (int, optional): The maximum sequence length for input prompts. Defaults to 512.
#         max_batch_size (int, optional): The maximum batch size for generating sequences. Defaults to 8.
#         max_gen_len (int, optional): The maximum length of generated sequences. If None, it will be
#             set to the model's max sequence length. Defaults to None.
#     """
#     generator = Llama.build(
#         ckpt_dir=ckpt_dir,
#         tokenizer_path=tokenizer_path,
#         max_seq_len=max_seq_len,
#         max_batch_size=max_batch_size,
#     )

def main(
    ckpt_dir: str,
    tokenizer_path: str,
    temperature: float = 0.6,
    top_p: float = 0.9,
    max_seq_len: int = 512,
    max_batch_size: int = 8,
    max_gen_len: Optional[int] = None,
    model_parallel_size: int = 1,
):
    """
    Entry point of the program for generating text using a pretrained model.

    Args:
        ckpt_dir (str): The directory containing checkpoint files for the pretrained model.
        tokenizer_path (str): The path to the tokenizer model used for text encoding/decoding.
        temperature (float, optional): The temperature value for controlling randomness in generation.
            Defaults to 0.6.
        top_p (float, optional): The top-p sampling parameter for controlling diversity in generation.
            Defaults to 0.9.
        max_seq_len (int, optional): The maximum sequence length for input prompts. Defaults to 512.
        max_batch_size (int, optional): The maximum batch size for generating sequences. Defaults to 8.
        max_gen_len (int, optional): The maximum length of generated sequences. If None, it will be
            set to the model's max sequence length. Defaults to None.
    """
    local_rank = int(os.getenv('LOCAL_RANK', 0))
    torch.cuda.set_device(local_rank)

    generator = Llama.build(
        ckpt_dir=ckpt_dir,
        tokenizer_path=tokenizer_path,
        max_seq_len=max_seq_len,
        max_batch_size=max_batch_size,
        model_parallel_size=model_parallel_size,
    )


    dialogs = []
    # One-shot
    for content in content_list:
        dialog = [{"role": "user", "content": 
        f"""   
        In machine learning projects, there are typically several core steps: Data Collection, Data Preprocessing, Feature Engineering, Model Training, Model Evaluation, Model Deployment and Model Monitoring. If a refactoring modifies code for one of these steps, it is considered a machine-learning-specific refactoring. For example, Refactoring Type: [Add Parameter],Original: _raw_face_locations_batched,Updated: _raw_face_locations_batched,Location:face_recognition/api.py,Description: [The parameters [ batch_size ] are added to the method _raw_face_locations_batched from the module face_recognition/api.py]. This is a machine-learning-specific refactoring. If it is unrelated to these steps and could also occur in non-machine-learning projects, it is considered a general refactoring. For example, Refactoring Type: [Change/Rename Parameter],Original: load_image_file,Updated: load_image_file,Location: face_recognition/api.py,Description: [The parameters [ filename ] of the method load_image_file from the module face_recognition/api.py are changed/renamed to [name]].This is a general refactoring. Classify the following refactorings as either machine-learning-specific or general. Answer with only one word: general or machine-learning-specific. {content}"""}]
        dialogs.append(dialog)


    results = generator.chat_completion(
        dialogs,  # type: ignore
        max_gen_len=max_gen_len,
        temperature=temperature,
        top_p=top_p,
    )

    for block, result in zip(refactoring_data, results):
    # Format the Llama result text into a list of lines
        lines_of_classification = format_classification_text(result['generation']['content'], width=100)
    # Add the list of lines as the "Classification" field
        block['Llama2 Classification'] = lines_of_classification


    # Save the updated data with classifications back to a new JSON file
    with open(output_file_path, 'w', encoding='utf-8') as file:
        json.dump(refactoring_data, file, ensure_ascii=False, indent=4)
    # for dialog, result in zip(dialogs, results):
    #     for msg in dialog:
    #         print(f"{msg['role'].capitalize()}: {msg['content']}\n")
    #     print(
    #         f"> {result['generation']['role'].capitalize()}: {result['generation']['content']}"
    #     )
    #     print("\n==================================\n")


if __name__ == "__main__":
    fire.Fire(main)
