"""
Hugging Face Hub Dataset Uploader
Client: Zarya Digital Bank (Pakistan)
Task: Task 5 — Upload dataset to private Hugging Face repo
"""

import os
import argparse
from huggingface_hub import HfApi, create_repo

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
CARD_PATH = os.path.join(BASE_DIR, "DATASET_CARD.md")

def upload_dataset(
    repo_id: str,
    token: str = None,
    private: bool = True
):
    """
    Creates and uploads the ZDB-UrduLish-v1 dataset to a private Hugging Face repository.
    """
    token = token or os.environ.get("HF_TOKEN")
    if not token:
        print("[!] HF_TOKEN not found in environment or arguments.")
        print("    Please provide --token <your_hf_write_token> or export HF_TOKEN='your_token'.")
        print("    Alternatively, run 'huggingface-cli login' in terminal.")
        return False

    api = HfApi(token=token)

    print(f"Creating repository '{repo_id}' (private={private}) on Hugging Face...")
    try:
        create_repo(
            repo_id=repo_id,
            repo_type="dataset",
            private=private,
            token=token,
            exist_ok=True
        )
        print(f"[+] Repository '{repo_id}' verified/created.")
    except Exception as e:
        print(f"[!] Warning while creating repository: {e}")

    files_to_upload = [
        (os.path.join(DATA_DIR, "train.jsonl"), "data/train.jsonl"),
        (os.path.join(DATA_DIR, "val.jsonl"), "data/val.jsonl"),
        (os.path.join(DATA_DIR, "golden_test_set.jsonl"), "data/golden_test_set.jsonl"),
        (os.path.join(DATA_DIR, "human_review_sample.csv"), "data/human_review_sample.csv"),
        (CARD_PATH, "README.md"),
    ]

    for local_path, repo_path in files_to_upload:
        if os.path.exists(local_path):
            print(f"Uploading {local_path} -> {repo_path}...")
            api.upload_file(
                path_or_fileobj=local_path,
                path_in_repo=repo_path,
                repo_id=repo_id,
                repo_type="dataset",
                token=token
            )
            print(f"  [+] Uploaded {repo_path} successfully.")
        else:
            print(f"  [!] Missing file: {local_path}")

    print(f"\n[DONE] Dataset successfully published to: https://huggingface.co/datasets/{repo_id}")
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload Zarya Bank dataset to Hugging Face Hub")
    parser.add_argument("--repo_id", type=str, default="zarya-bank/urdulish-banking-assistant", help="HF dataset repo ID (e.g. username/repo-name)")
    parser.add_argument("--token", type=str, default=None, help="Hugging Face User Access Token with write permissions")
    parser.add_argument("--public", action="store_true", help="Make repository public instead of private")
    
    args = parser.parse_args()
    upload_dataset(repo_id=args.repo_id, token=args.token, private=not args.public)
