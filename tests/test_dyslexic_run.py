import sys
from unittest.mock import MagicMock

# Mock heavy dependencies before they are imported
sys.modules['transformers'] = MagicMock()
sys.modules['torch'] = MagicMock()

import unittest
from unittest.mock import patch

# Ensure backend is in path so internal imports work
if 'backend' not in sys.path:
    sys.path.append('backend')

# Import modules
import dyslexic_logic
import suggestion_pipeline
import context_engine

class TestDyslexicRun(unittest.TestCase):
    def test_generate_candidates_phonetic(self):
        """Test that phonetic matches are found."""
        dictionary = ["friend", "field", "fry", "end", "school", "cool"]
        # "frend" sounds like "friend"
        candidates = dyslexic_logic.generate_candidates("frend", dictionary, top_n=5)
        self.assertIn("friend", candidates)

    def test_generate_candidates_visual(self):
        """Test that visual matches are found."""
        dictionary = ["friend", "fiend", "fended"]
        # "fiend" looks like "friend" (one letter diff)
        candidates = dyslexic_logic.generate_candidates("friend", dictionary, top_n=5)
        self.assertIn("fiend", candidates)

    def test_generate_candidates_no_match(self):
        """Test that no match returns empty list."""
        dictionary = ["apple", "banana"]
        candidates = dyslexic_logic.generate_candidates("xyz", dictionary, top_n=5)
        self.assertEqual(candidates, [])

    def test_rerun_consistency(self):
        """Test that running the same input multiple times yields same result (idempotency)."""
        dictionary = ["friend", "field", "fry"]
        run1 = dyslexic_logic.generate_candidates("frend", dictionary, top_n=5)
        run2 = dyslexic_logic.generate_candidates("frend", dictionary, top_n=5)
        self.assertEqual(run1, run2)

    @patch('context_engine.ContextRanker')
    @patch('suggestion_pipeline.profile_manager')
    @patch('suggestion_pipeline.comprehension_service')
    def test_full_pipeline_mocked(self, mock_cs, mock_pm, MockRanker):
        """Test the full suggestion pipeline with mocked dependencies."""

        # Mock Context Ranker
        mock_instance = MockRanker.return_value
        mock_instance.rank_candidates.return_value = [
            {'word': 'friend', 'score': 0.9, 'confidence_pct': 90.0},
            {'word': 'field', 'score': 0.1, 'confidence_pct': 10.0}
        ]

        # Mock Profile Manager
        mock_pm.data = {"lexicon": []}
        mock_pm.get_personalization_factor.return_value = 1.0
        mock_pm.get_ui_recommendations.return_value = {}

        # Mock Comprehension Service
        mock_cs.get_comprehension_aid.return_value = {
            "example": "This is a friend.",
            "definition": "A pal.",
            "audio_endpoint": "http://audio"
        }
        mock_cs.generate_homophone_warning.return_value = None

        dictionary = ["friend", "field"]

        # Test input
        result = suggestion_pipeline.get_robust_suggestions(
            "My frend is here.", "frend", dictionary
        )

        # Assertions
        self.assertEqual(result['status'], 'success')
        self.assertEqual(len(result['suggestions']), 2)
        suggestions = [s['word'] for s in result['suggestions']]
        self.assertIn('friend', suggestions)
        self.assertIn('%', result['suggestions'][0]['confidence'])

if __name__ == "__main__":
    unittest.main()
