# Copyright (c) Meta Platforms, Inc. and affiliates.
# This software may be used and distributed according to the terms of the Llama 2 Community License Agreement.

from typing import List, Optional

import fire

from llama import Llama, Dialog

import json
import os
import textwrap

# Path to JSON file
json_file_path = '/mimer/NOBACKUP/groups/2023-llm-refactoring/PyRef/face_recognition_data_with_classification_with_gpt_classification.json'
# output_json_suffix = '_with_fewshot_classification.json'
output_json_suffix = '_short.json'

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



def main(
    ckpt_dir: str,
    tokenizer_path: str,
    temperature: float = 0.6,
    top_p: float = 0.9,
    max_seq_len: int = 512,
    max_batch_size: int = 8,
    max_gen_len: Optional[int] = None,
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
    generator = Llama.build(
        ckpt_dir=ckpt_dir,
        tokenizer_path=tokenizer_path,
        max_seq_len=max_seq_len,
        max_batch_size=max_batch_size,
    )

    dialogs = []
    # One-shot
    # for content in content_list:
    #     dialog = [{"role": "user", "content": f"Is this a machine learning specific software refactoring or a general software refactoring? {content}"}]
    #     dialogs.append(dialog)
    
    # Few-shot with examples
    for content in content_list:
        dialog = [{"role": "user", "content": 
        f"""   
         "Refactoring Type": [
            "Add Parameter"
        ],
        "Original": "_merge_on_cpu",
        "Updated": "_merge_on_cpu",
        "Location": "apps/DeepFaceLive/backend/FaceMerger.py/FaceMergerWorker",
        "Original Line": 174,
        "Updated Line": 185,
        "Description": [
            "The parameters [ face_align_img ] are added to the method _merge_on_cpu from the module apps/DeepFaceLive/backend/FaceMerger.py in class FaceMergerWorker"
        ],
        "Commit": "03547088c6453b9c05931020a33d4640d7cd75f2",
        "Classification": [" Machine-learning specific software refactoring"]

        
         "Refactoring Type": [
            "Change Return Type"
        ],
        "Original": "get_files_paths",
        "Updated": "get_files_paths",
        "Location": "xlib/path/path.py",
        "Original Line": 25,
        "Updated Line": 26,
        "Description": [
            "The return type of method get_files_paths from the module xlib/path/path.py is updated"
        ],
        "Commit": "2605930dfea8db970f884a4f729784f3586173d4",
        "Classification": [" General software refactoring"]

        
        "Refactoring Type": [
            "Rename Method"
        ],
        "Original": "_free_random_pooled_buffers",
        "Updated": "_release_random_pooled_buffers",
        "Location": "xlib/avecl/_internal/backend/Device.py/Device",
        "Original Line": 205,
        "Updated Line": 205,
        "Description": [
            "The method _free_random_pooled_buffers from the module xlib/avecl/_internal/backend/Device.py in class Device is renamed to _release_random_pooled_buffers"
        ],
        "Commit": "2d401f47f87de9fdbea2f04a4f268c9d180f39d6"
         "Classification": [ " General software refactoring" ]

        

         "Refactoring Type": [
            "Rename Method"
        ],
        "Original": "get_compute_capability",
        "Updated": "get_execution_provider",
        "Location": "xlib/onnxruntime/device.py/ORTDeviceInfo",
        "Original Line": 30,
        "Updated Line": 35,
        "Description": [
            "The method get_compute_capability from the module xlib/onnxruntime/device.py in class ORTDeviceInfo is renamed to get_execution_provider"
        ],
        "Commit": "6d504d596904b1f68349fa3535e09b69484eca98",
        "Classification": [" Machine-learning specific software refactoring"]

         "Refactoring Type": [
            "Rename Method"
        ],
        "Original": "get_compute_capability",
        "Updated": "get_execution_provider",
        "Location": "xlib/onnxruntime/device.py/ORTDeviceInfo",
        "Original Line": 30,
        "Updated Line": 35,
        "Description": [
            "The method get_compute_capability from the module xlib/onnxruntime/device.py in class ORTDeviceInfo is renamed to get_execution_provider"
        ],
        "Commit": "6d504d596904b1f68349fa3535e09b69484eca98",
        "Classification": [" Machine-learning specific software refactoring"]

         "Refactoring Type": [
            "Rename Method"
        ],
        "Original": "get_compute_capability",
        "Updated": "get_execution_provider",
        "Location": "xlib/onnxruntime/device.py/ORTDeviceInfo",
        "Original Line": 30,
        "Updated Line": 35,
        "Description": [
            "The method get_compute_capability from the module xlib/onnxruntime/device.py in class ORTDeviceInfo is renamed to get_execution_provider"
        ],
        "Commit": "6d504d596904b1f68349fa3535e09b69484eca98",
        "Classification": [" Machine-learning specific software refactoring"]

        
        Classify this refactoring to general software refactoring or machine-learning specific software refactoring.
        Answer with Machine-learning specific software refactoring or General software refactoring{content}"""}]
        dialogs.append(dialog)

        # General software refactoring Description:The return type of method get_files_paths from the module xlib/path/path.py is updated
        # Machine-learning specific software refactoring Description:The parameters face_align_img are added to the method _merge_on_cpu from the module apps/DeepFaceLive/backend/FaceMerger.py in class FaceMergerWorker

    # for content in content_list:
    #     dialog = [{"role": "user", "content": 
    #     f"""   
    #     General software refactoring Description:The return type of method get_files_paths from the module xlib/path/path.py is updated
    #     Machine-learning specific software refactoring Description:The parameters face_align_img are added to the method _merge_on_cpu from the module apps/DeepFaceLive/backend/FaceMerger.py in class FaceMergerWorker
    #     Classify this refactoring to machine-learning specific or general. Answer me only with one word: General or ML-specific. {content}"""}]
    #     dialogs.append(dialog)

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
        block['Llama Classification'] = lines_of_classification


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
