---
license: mit
task_categories:
- text-generation
language:
- en
tags:
- typo
pretty_name: M2M
size_categories:
- 10K<n<100K
---

# Clear Spelling Dataset

## Overview

The **Mistake to Meaning** (M2M) dataset is a carefully crafted synthetic collection of **100,000 unique English spelling mistakes and their correct forms**, intended for training high-quality typo correction and spell checking AI models. It covers various types of common mistakes observed frequently in real-world scenarios, such as:

- Keyboard adjacency typos
- Letter swaps and omissions
- Duplicate characters
- Phonetic substitution errors
- Commonly confused homophones (e.g., "their" vs. "there")

## Dataset Format

The dataset is provided in **CSV format** with two clearly defined columns:

| Column   | Description                                 | Example             |
|----------|---------------------------------------------|---------------------|
| `error`  | The misspelled or incorrect word or phrase  | "teh"              |
| `correct`| The correct word or intended phrase         | "the"              |

## Usage

This dataset is ideal for:

- Training and fine-tuning **typo correction** models
- Benchmarking **spell-checking algorithms**
- Enhancing NLP model robustness to real-world noisy input

## Quality Assurance

- **No duplicates:** Each (error, correct) pair is unique.
- **Hand-curated seed set:** Includes hundreds of common misspellings verified against real-world usage patterns.
- **Realistic noise generation:** Uses realistic error transformations mimicking genuine human typing behavior.

## License (MIT)

This dataset is released under the permissive **MIT License**, which allows commercial and non-commercial use, distribution, and modification. Attribution is required:


## Citation

If you use this dataset in your research or projects, please provide attribution similar to:

```
This [your project type] uses the Mistake to Learning dataset by ProCreations.
```

Enjoy training your typo-correction models!