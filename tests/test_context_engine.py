import pytest
import sys
import os
from unittest.mock import MagicMock

# Mock the heavy transformer pipeline so tests are fast
sys.modules['transformers'] = MagicMock()
sys.modules['torch'] = MagicMock()

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))
from context_engine import ContextRanker

def test_windowing_logic():
    ranker = ContextRanker()
    # If the sentence is huge, it should cut it down
    long_sentence = "word " * 600
    # Mocking the tokenizer attribute access
    ranker._pipeline = MagicMock()
    ranker._pipeline.tokenizer.mask_token = "<mask>"
    
    # Test the internal window function
    masked = f"Start of sentence {ranker._pipeline.tokenizer.mask_token} end."
    windowed = ranker._window_sentence(masked, context_size=5)
    
    # Ensure it didn't crash and kept the mask
    assert "<mask>" in windowed
