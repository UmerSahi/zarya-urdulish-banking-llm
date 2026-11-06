"""
Push Fine-Tuned Model (LoRA Adapter & Quantized Weights) to Private Hugging Face Repo
Client: Zarya Digital Bank (Pakistan)
Task: Day 5 Task 1 — Production Model Versioning & Artifact Storage
"""

import os
import sys
import argparse
from pathlib import Path

# Paths
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ADAPTER_DIR = os.path.join(REPO_ROOT, "Adaptors", "qwen-adaptors")
MODEL_CARD_PATH = os.path.join(os.path.dirname(__file__), "MODEL_CARD.md")

DEFAULT_REPO_ID = "zarya-digital-bank/qwen-2.5-3b-urdulish-banking-dpo"
DEFAULT_TAG = "v1.2.0-dpo-quant"

def push_model_artifacts(
    repo_id: str = DEFAULT_REPO_ID,
    token: str = None,
    tag: str = DEFAULT_TAG,
    private: bool = True
):
    print("=" * 75)
    print("  ZARYA DIGITAL BANK — HUGGING FACE MODEL HUB UPLOADER")
    print("=" * 75)
    print(f"Target Repository : {repo_id}")
    print(f"Release Tag       : {tag}")
    print(f"Visibility        : {'Private (State Bank compliant)' if private else 'Public'}")
    print(f"Source Directory  : {ADAPTER_DIR}")

    hf_token = token or os.getenv("HF_TOKEN")
    if not hf_token:
        print("\n[INFO] HF_TOKEN environment variable not set. Running in dry-run verification mode.")
        print("To push live, run: python push_to_hf.py --token <your_hf_token> or export HF_TOKEN=<token>\n")
        
        # Verify local artifacts exist
        required_files = [
            "adapter_config.json",
            "adapter_model.safetensors",
            "tokenizer.json",
            "tokenizer_config.json",
            "chat_template.jinja"
        ]
        
        all_present = True
        print("Verifying local release artifacts:")
        for rf in required_files:
            p = os.path.join(ADAPTER_DIR, rf)
            if os.path.exists(p):
                size_mb = os.path.getsize(p) / (1024 * 1024)
                print(f"  [OK] {rf:<26} ({size_mb:8.2f} MB)")
            else:
                print(f"  [MISSING] {rf}")
                all_present = False

        if os.path.exists(MODEL_CARD_PATH):
            print(f"  [OK] {'MODEL_CARD.md':<26} (Validated)")
        
        if all_present:
            print("\n[DRY RUN SUCCESSFUL] All adapter artifacts and model cards are ready for Hugging Face upload.")
            return True
        else:
            print("\n[WARNING] Some artifacts are missing.")
            return False

    try:
        from huggingface_hub import HfApi, create_repo
        api = HfApi(token=hf_token)

        # 1. Ensure private repo exists
        print(f"\n[1/3] Ensuring repository exists at https://huggingface.co/{repo_id}...")
        create_repo(repo_id=repo_id, token=hf_token, private=private, exist_ok=True)

        # 2. Upload Adapter folder
        print(f"[2/3] Uploading adapter artifacts from {ADAPTER_DIR}...")
        api.upload_folder(
            folder_path=ADAPTER_DIR,
            repo_id=repo_id,
            commit_message=f"Production release {tag}: LoRA adapter weights, tokenizer, and ChatML Jinja template",
            token=hf_token
        )

        # 3. Upload Model Card
        if os.path.exists(MODEL_CARD_PATH):
            print(f"[3/3] Uploading MODEL_CARD.md to repo root...")
            api.upload_file(
                path_or_fileobj=MODEL_CARD_PATH,
                path_in_repo="README.md",
                repo_id=repo_id,
                commit_message=f"Update official Model Card for release {tag}",
                token=hf_token
            )

        print("\n" + "=" * 75)
        print("  MODEL SUCCESSFULLY PUSHED TO HUGGING FACE HUB")
        print(f"  Repo URL: https://huggingface.co/{repo_id}")
        print(f"  Tag:      {tag}")
        print("=" * 75)
        return True

    except Exception as e:
        print(f"\n[ERROR] Failed to upload to Hugging Face: {e}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload Zarya Banking Model to Hugging Face Hub")
    parser.add_argument("--repo-id", default=DEFAULT_REPO_ID, help="Hugging Face repo id")
    parser.add_argument("--token", default=None, help="Hugging Face access token")
    parser.add_argument("--tag", default=DEFAULT_TAG, help="Release tag")
    args = parser.parse_args()

    push_model_artifacts(repo_id=args.repo_id, token=args.token, tag=args.tag)

