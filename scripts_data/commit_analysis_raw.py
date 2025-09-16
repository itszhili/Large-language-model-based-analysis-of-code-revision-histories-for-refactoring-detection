import git
from llama import Llama, Dialog
import json
from typing import List, Optional
import fire

def analyze_commit(commit, generator, temperature, top_p, max_gen_len):

    if commit.parents:
        diff = commit.diff(commit.parents[0], create_patch=True)
    else:
        diff = commit.diff(None, create_patch=True)

    diff_text = '\n'.join([d.diff.decode('utf-8') for d in diff])

    # Preparing the question for the LLaMA2 model
    question = f"What are the refactorings in this commit: {commit.hexsha}? Are they machine learning specific or general?"

    # Creating the dialog in the specified format
    dialogs = [{"role": "user", "content": diff_text + " " + question}]
        
    results = generator.chat_completion(
        dialogs,  # type: ignore
        max_gen_len=max_gen_len,
        temperature=temperature,
        top_p=top_p,
    )

    for result in results:
        print(
            f"> {result['generation']['role'].capitalize()}: {result['generation']['content']}"
        )
        print("\n==================================\n")

    return results

def main(
    repo_path: str,
    ckpt_dir: str,
    tokenizer_path: str,
    temperature: float = 0.6,
    top_p: float = 0.9,
    max_seq_len: int = 512,
    max_batch_size: int = 8,
    max_gen_len: Optional[int] = None,
):
    repo_path = "/cephyr/users/zhil/Alvis/repos/faceswap"
    # Initialize the LLaMA2 model
    generator = Llama.build(
        ckpt_dir=ckpt_dir,
        tokenizer_path=tokenizer_path,
        max_seq_len=max_seq_len,
        max_batch_size=max_batch_size,
    )

    # Initialize the git repository
    repo = git.Repo(repo_path)

    commit_analysis = []

    # Iterate through the commits
    for commit in repo.iter_commits():
        analysis_results = analyze_commit(commit, generator, temperature, top_p, max_gen_len)
        commit_data = {
            'commit_id': commit.hexsha,
            'message': commit.message.strip(),
            'analysis': analysis_results
        }
        commit_analysis.append(commit_data)

    # Save the analysis results to a file
    with open('commit_analysis.json', 'w') as file:
        json.dump(commit_analysis, file, indent=4)

if __name__ == "__main__":
    fire.Fire(main)