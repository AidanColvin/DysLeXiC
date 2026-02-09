from huggingface_hub import snapshot_download
import os

datasets = [
    ("ProCreations/Mistake-To-Meaning", "data/m2m"),
    ("gpric024/wmt14_injected_synthetic_dyslexia", "data/wmt14_dyslexia"),
    ("SPEAK-ASR/sinhala-dyslexia-corrected-id20percent", "data/sinhala_dyslexia")
]

for repo_id, local_dir in datasets:
    print(f"Downloading {repo_id}...")
    snapshot_download(
        repo_id=repo_id, 
        repo_type="dataset", 
        local_dir=local_dir, 
        local_dir_use_symlinks=False
    )
    print(f"Finished {repo_id}")
