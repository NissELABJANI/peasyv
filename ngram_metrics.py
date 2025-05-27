import json
from collections import Counter
from nltk.util import ngrams

def ngram_metrics(txt_path, json_path):
    with open(txt_path, 'r', encoding='utf-8') as f:
        words = [line.strip() for line in f if line.strip()]

    total_words = len(words)
    unique_words = len(set(words))
    type_token_ratio = round(unique_words / total_words, 3) if total_words else 0.0

    bigrams = list(ngrams(words, 2))
    trigrams = list(ngrams(words, 3))

    top_bigrams = Counter(bigrams).most_common(5)
    top_trigrams = Counter(trigrams).most_common(5)

    data = {
        "total_words": total_words,
        "unique_words": unique_words,
        "type_token_ratio": type_token_ratio,
        "top_bigrams": [[w1, w2, count] for ((w1, w2), count) in top_bigrams],
        "top_trigrams": [[w1, w2, w3, count] for ((w1, w2, w3), count) in top_trigrams],
    }

    with open(json_path, 'w', encoding='utf-8') as out:
        json.dump(data, out, indent=2)

    return data
