import pandas as pd
import json
import os
import glob

output_file = "standardized_training_data.jsonl"
data_rows = []

# 1. Process Sinhala Parquet (Corrected vs Dyslexic)
sinhala_path = "data/sinhala_dyslexia/data/train-00000-of-00001.parquet"
if os.path.exists(sinhala_path):
    print("Processing Sinhala Parquet...")
    df = pd.read_parquet(sinhala_path)
    # Mapping based on common ASR/Dyslexia dataset schemas
    # Adjust column names if your 'ls' reveals different headers
    for _, row in df.iterrows():
        data_rows.append({
            "original_text": row.get('dyslexic_text', row.get('transcript', '')),
            "corrected_text": row.get('corrected_text', row.get('ground_truth', ''))
        })

# 2. Process M2M CSV
m2m_path = "data/m2m/Mistake to Meaning.csv"
if os.path.exists(m2m_path):
    print("Processing M2M CSV...")
    df_m2m = pd.read_csv(m2m_path)
    for _, row in df_m2m.iterrows():
        data_rows.append({
            "original_text": row.get('Mistake', ''),
            "corrected_text": row.get('Meaning', '')
        })

# 3. Process WMT14 TXT Files (Mapping Synthetic to Original)
# We assume the .txt files in English_input_data contain the synthetic (original_text)
# and we compare them against the clean baseline (wmt14_en...0.0_p_letter_0.0...txt)
wmt_dir = "data/wmt14_dyslexia/Data/English_input_data/"
baseline_file = os.path.join(wmt_dir, "wmt14_en_p_homophone_0.0_p_letter_0.0_p_confusing_word_0.0.txt")

if os.path.exists(baseline_file):
    print("Processing WMT14 Synthetic TXTs...")
    with open(baseline_file, 'r', encoding='utf-8') as f:
        clean_lines = f.readlines()
    
    # Grab all other synthetic variation files
    synthetic_files = glob.glob(os.path.join(wmt_dir, "*.txt"))
    for s_file in synthetic_files:
        if "0.0_p_letter_0.0_p_confusing_word_0.0" in s_file: continue
        with open(s_file, 'r', encoding='utf-8') as f:
            synthetic_lines = f.readlines()
        
        # Zip them together so each synthetic line matches its clean version
        for synth, clean in zip(synthetic_lines, clean_lines):
            if synth.strip() and clean.strip():
                data_rows.append({
                    "original_text": synth.strip(),
                    "corrected_text": clean.strip()
                })

# Save to JSONL
with open(output_file, 'w', encoding='utf-8') as f:
    for entry in data_rows:
        f.write(json.dumps(entry) + '\n')

print(f"Successfully created {output_file} with {len(data_rows)} rows.")
