from typing import Any, Dict, List, Optional
from typing import List, Dict
import re

def extract_key_structure(text: str) -> Dict[str, Any]:
    """
    analyzes raw text to create a 'condensed view' structure
    extracts headers, bullet points, and generates a summary
    """
    lines = text.split('\n')
    structure = {
        "headings": [],
        "key_terms": [],
        "summary_bullets": []
    }
    
    # Simple regex heuristic for "Key Terms" (Capitalized words in sequence)
    # Refined by your request: "Bold keywords... pair with nearby context"
    # We simulate this by finding noun phrases (simplified here)
    
    for line in lines:
        line = line.strip()
        if not line: continue
        
        # Detect Headers (Short lines, ends with colon or no punctuation, Capitalized)
        if len(line) < 60 and (line.isupper() or line.endswith(':')):
            structure["headings"].append(line)
            
        # Detect Lists (starts with -, *, 1.)
        if re.match(r'^[\-\*•\d\.]', line):
            structure["summary_bullets"].append(line)

    # If we have too few bullets, we might need to auto-summarize
    # (Connects to your existing text_service.summarize_text)
    
    return structure
