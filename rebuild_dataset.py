import pandas as pd
import json
import os
import glob

output_file = "standardized_training_data.jsonl"
data_rows = []

def add_pair(orig, corr):
    if orig and corr and str(orig).strip() and str(corr).strip():
        data_rows.append({"original_text": str(orig).strip(), "corrected_text": str(corr).strip()})

# 1. Sinhala & M2M (Existing logic but with cleaner checks)
if os.path.exists("data/m2m/Mistake to Meaning.csv"):
    df = pd.read_csv("data/m2m/Mistake to Meaning.csv")
    for _, r in df.iterrows():
        add_pair(r.get('Mistake'), r.get('Meaning'))

# 2. Process ALL WMT14 Text files (English & French GPT/Google)
# Using the 0.0 file as the anchor/target for everything in those folders
search_dirs = [
    "data/wmt14_dyslexia/Data/English_input_data/",
    "data/wmt14_dyslexia/Data/French_translated_data/google/",
    "data/wmt14_dyslexia/Data/French_translated_data/gpt/"
]

for d in search_dirs:
    if not os.path.exists(d): continue
    # Find the 'clean' file (0.0 noise) to use as Target
    baseline = glob.glob(os.path.join(d, "*0.0_p_letter_0.0*"))
    if not baseline: continue
    
    with open(baseline[0], 'r', encoding='utf-8') as f:
        clean_lines = f.readlines()
    
    for s_file in glob.glob(os.path.join(d, "*.txt")):
        if s_file == baseline[0]: continue
        with open(s_file, 'r', encoding='utf-8') as f:
            noisy_lines = f.readlines()
        for noisy, clean in zip(noisy_lines, clean_lines):
            add_pair(noisy, clean)

with open(output_file, 'w', encoding='utf-8') as f:
    for entry in data_rows:
        f.write(json.dumps(entry) + '\n')

print(f"Dataset rebuilt: {len(data_rows)} valid rows saved.")
