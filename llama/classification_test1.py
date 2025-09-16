# Copyright (c) Meta Platforms, Inc. and affiliates.
# This software may be used and distributed according to the terms of the Llama 2 Community License Agreement.

from typing import List, Optional

import fire

from llama import Llama, Dialog

import json

# Path to JSON file
json_file_path = '/mimer/NOBACKUP/groups/2023-llm-refactoring/PyRef/attention-ocr_data.json'

with open(json_file_path, 'r') as file:
    refactoring_data = json.load(file)

content_list = []

for block in refactoring_data:
    content = (f"Refactoring Type: {block['Refactoring Type']}, "
               f"Original: {block['Original']}, "
               f"Updated: {block['Updated']}, "
               f"Location: {block['Location']}, "
               f"Description: {block['Description']}, "
               f"Commit: {block['Commit']}")
    content_list.append(content)


# for content in content_list:
#     print(content)


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

    # dialogs: List[Dialog] = [
    #         [{"role": "user", "content": "Is this a machine learning specific software refactoring or a general software refactoring? Refactoring Type: Add Parameter,Original: load_aligned,Updated: load_aligned,Location: lib/faces_detect.py/DetectedFace,Original Line: 219,Updated Line: 219,Description: The parameters  force  are added to the method load_aligned from the module lib/faces_detect.py in class DetectedFace,Commit: 00068f84515dd52e3f6b57b05bc0f33987946b58"}],
    #         [{"role": "user", "content": "what is the captical city of Sweden?"}],
    # ]
    dialogs = []
    for content in content_list:
        dialog = [{"role": "user", "content": f"Is this a machine learning specific software refactoring or a general software refactoring? {content}"}]
        dialogs.append(dialog)
   
    results = generator.chat_completion(
        dialogs,  # type: ignore
        max_gen_len=max_gen_len,
        temperature=temperature,
        top_p=top_p,
    )

    for dialog, result in zip(dialogs, results):
        for msg in dialog:
            print(f"{msg['role'].capitalize()}: {msg['content']}\n")
        print(
            f"> {result['generation']['role'].capitalize()}: {result['generation']['content']}"
        )
        print("\n==================================\n")


if __name__ == "__main__":
    fire.Fire(main)
