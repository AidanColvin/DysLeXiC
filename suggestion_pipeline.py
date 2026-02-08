from typing import List, Dict, Any
import logging

# Import our robust modules
import dyslexic_logic
import context_engine
import user_profile
import comprehension_service

logger = logging.getLogger(__name__)

# Initialize User Profile Manager
profile_manager = user_profile.UserProfileManager()

def get_robust_suggestions(sentence: str, misspelled_word: str, dictionary: List[str]) -> Dict[str, Any]:
    """
    The Master Pipeline:
    1. Generate Candidates (Phonetic + Visual Distance)
    2. Context Rank (BERT)
    3. Personalization Rank (User History)
    4. Enrich (Add Audio/Examples)
    5. Truncate (Top 3)
    """
    
    # --- Step 0: Check Ignore List ---
    if misspelled_word in profile_manager.data["lexicon"]:
        return {"status": "ignored", "suggestions": []}

    # --- Step 1: Broad Candidate Generation ---
    # Using the robust logic from dyslexic_logic.py
    candidates = dyslexic_logic.generate_candidates(misspelled_word, dictionary, top_n=20)
    
    if not candidates:
        return {"status": "no_match", "suggestions": []}

    # --- Step 2: Contextual Ranking (BERT) ---
    # Get scores 0.0 to 1.0 based on sentence fit
    ranked_candidates = context_engine.rank_candidates_by_context(sentence, misspelled_word, candidates)

    # --- Step 3: Personalization Re-Ranking ---
    # Multiply BERT score by User Profile weight
    final_ranking = []
    
    for item in ranked_candidates:
        word = item['word']
        base_score = item['score']
        
        # Apply user multiplier (e.g. * 1.2 if they use this word often)
        user_multiplier = profile_manager.get_personalization_factor(word, misspelled_word)
        final_score = base_score * user_multiplier
        
        final_ranking.append({
            "word": word,
            "score": final_score,
            "debug_base": base_score,
            "debug_mult": user_multiplier
        })

    # Sort by final score
    final_ranking.sort(key=lambda x: x['score'], reverse=True)

    # --- Step 4: Truncate (Encourage Proofreading) ---
    # Keep only top 3 to reduce cognitive load
    top_picks = final_ranking[:3]

    # --- Step 5: Comprehension Enrichment ---
    # Add examples and audio links for the top picks
    enriched_results = []
    for item in top_picks:
        word = item['word']
        aid_data = comprehension_service.get_comprehension_aid(word)
        
        suggestion_entry = {
            "word": word,
            "confidence": f"{int(item['score'] * 100)}%",
            "example_sentence": aid_data["example"],
            "definition_snippet": aid_data["definition"][:50] + "...", # Keep it short
            "audio_preview_url": aid_data["audio_endpoint"],
            "homophone_hint": comprehension_service.generate_homophone_warning(word)
        }
        enriched_results.append(suggestion_entry)

    # Return package with UI hints
    return {
        "status": "success",
        "suggestions": enriched_results,
        "ui_adaptations": profile_manager.get_ui_recommendations()
    }

def handle_user_feedback(misspelling: str, chosen_word: str, action: str):
    """
    Endpoint handler for when user clicks a suggestion or 'Ignore'
    action: 'accepted' | 'ignored'
    """
    if action == 'ignored':
        profile_manager.add_to_lexicon(misspelling)
    elif action == 'accepted':
        profile_manager.learn_from_correction(misspelling, chosen_word)
