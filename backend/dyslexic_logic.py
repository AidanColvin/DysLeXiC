import re
from metaphone import doublemetaphone
from Levenshtein import distance as levenshtein_distance

class DyslexicAssistant:
    def __init__(self):
        self.correction_map = {
            "becuase": "because",
            "dont": "don't",
            "didnt": "didn't",
            "cant": "can't",
            "wont": "won't",
            "isnt": "isn't",
            "arent": "aren't",
            "couldnt": "couldn't",
            "shouldnt": "shouldn't",
            "frend": "friend",
            "teh": "the"
        }

    def correct_text(self, text):
        words = re.findall(r"[\w']+|[.,!?;]", text)
        corrected_words = []
        for word in words:
            lower_word = word.lower()
            if lower_word in self.correction_map:
                replacement = self.correction_map[lower_word]
                if word[0].isupper():
                    replacement = replacement.capitalize()
                corrected_words.append(replacement)
            else:
                corrected_words.append(word)
        result = " ".join(corrected_words)
        for char in [".", ",", "!", "?", ";"]:
            result = result.replace(f" {char}", char)
        return result

def generate_candidates(misspelled_word, dictionary, top_n=20):
    """
    Generates a list of candidate words based on phonetic similarity and visual distance.
    """
    if not misspelled_word:
        return []

    # Optimization: Filter candidates by length first
    misspelled_len = len(misspelled_word)
    # Only consider words within length +/- 2 (Levenshtein lower bound)
    candidates_by_len = [
        w for w in dictionary
        if abs(len(w) - misspelled_len) <= 2
    ]

    target_phonetic = doublemetaphone(misspelled_word)
    scored_candidates = []

    for word in candidates_by_len:
        # Check if primary or secondary phonetic codes match
        word_phonetic = doublemetaphone(word)
        phonetic_match = False

        # doublemetaphone returns tuple (primary, secondary)
        # Ensure we don't compare None or empty strings unless valid
        if (target_phonetic[0] and target_phonetic[0] == word_phonetic[0]) or \
           (target_phonetic[1] and target_phonetic[1] == word_phonetic[1]):
            phonetic_match = True

        # Only compute Levenshtein distance if phonetics match OR length is very close
        # (Length filter already applied, so we are safe to compute distance on remaining set)
        dist = levenshtein_distance(misspelled_word, word)

        if phonetic_match:
            scored_candidates.append((word, dist))
        elif dist <= 2:
            # If visual distance is small, consider it even if phonetics don't match
            scored_candidates.append((word, dist))

    # Deduplicate and sort
    unique_candidates = {}
    for word, dist in scored_candidates:
        if word not in unique_candidates or dist < unique_candidates[word]:
            unique_candidates[word] = dist

    final_candidates = sorted(unique_candidates.items(), key=lambda x: x[1])

    return [word for word, dist in final_candidates[:top_n]]
