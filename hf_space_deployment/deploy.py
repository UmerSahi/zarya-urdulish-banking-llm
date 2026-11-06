"""
One-Click Hugging Face Spaces Deployment Script
Client: Zarya Digital Bank (Pakistan)
Week 10 Capstone — Day 5: Production Deployment with Live Link
"""

import os
import sys
import argparse
from pathlib import Path

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

def deploy_to_huggingface_space(token: str, username: str = None, space_name: str = "zarya-urdulish-banking-assistant"):
    print("=" * 75)
    print("  ZARYA DIGITAL BANK — HUGGING FACE SPACES DEPLOYER")
    print("=" * 75)

    try:
        from huggingface_hub import HfApi, create_repo, whoami
    except ImportError:
        print("[Error] huggingface_hub not installed. Run: pip install huggingface_hub")
        return False

    api = HfApi(token=token)

    # 1. Identify User
    try:
        user_info = whoami(token=token)
        hf_user = username or user_info.get("name")
        print(f"[Authenticated] Hugging Face User: @{hf_user}")
    except Exception as e:
        print(f"[Auth Error] Invalid Hugging Face Token: {e}")
        print("Please generate a Write Token at: https://huggingface.co/settings/tokens")
        return False

    space_id = f"{hf_user}/{space_name}"
    print(f"[Target Space] https://huggingface.co/spaces/{space_id}")

    # 2. Create Space Repository
    print(f"\n[1/2] Creating/Verifying Hugging Face Space repository...")
    try:
        create_repo(
            repo_id=space_id,
            repo_type="space",
            space_sdk="streamlit",
            token=token,
            exist_ok=True
        )
        print("  [OK] Space repository initialized.")
    except Exception as e:
        print(f"  [Notice] Repository check: {e}")

    # 3. Upload Application Files
    print(f"\n[2/2] Uploading application files from {CURRENT_DIR}...")
    try:
        api.upload_folder(
            folder_path=CURRENT_DIR,
            repo_id=space_id,
            repo_type="space",
            token=token,
            commit_message="Deploy production Zarya UrduLish Banking Assistant with SBP Guardrails & CRM"
        )
        print("\n" + "=" * 75)
        print("  DEPLOYMENT SUCCESSFUL!")
        print(f"  Live Space URL : https://huggingface.co/spaces/{space_id}")
        print("  App will be online in ~60-90 seconds as Hugging Face builds the container.")
        print("=" * 75)
        return f"https://huggingface.co/spaces/{space_id}"
    except Exception as e:
        print(f"[Upload Error] Failed to upload files: {e}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Deploy to Hugging Face Spaces")
    parser.add_argument("--token", default=os.getenv("HF_TOKEN"), help="Hugging Face Write Token")
    parser.add_argument("--space-name", default="zarya-urdulish-banking-assistant", help="Name for your Space")
    args = parser.parse_args()

    token = args.token
    if not token:
        print("Hugging Face Write Token required.")
        token = input("Enter your Hugging Face Token (starts with hf_...): ").strip()

    deploy_to_huggingface_space(token=token, space_name=args.space_name)

