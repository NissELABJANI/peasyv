import re
import sys

def clean_word_line(line):
    # Remove embedded timestamps like <00:00:01.120>
    line = re.sub(r'<\d{2}:\d{2}:\d{2}\.\d{3}>', '', line)
    # Remove <c> tags and things like [Music]
    line = re.sub(r'<[^>]+>', '', line)
    line = re.sub(r'\[.*?\]', '', line)
    return line.strip()

def vtt_to_words(vtt_path, txt_path):
    words = []
    with open(vtt_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # Skip timestamps and headers
            if "-->" in line or line.startswith("WEBVTT") or line.startswith("Kind:") or line.startswith("Language:") or not line:
                continue
            cleaned = clean_word_line(line)
            for word in cleaned.split():
                words.append(word)
    with open(txt_path, 'w', encoding='utf-8') as out:
        out.write("\n".join(words))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python vtt.py input.vtt output.txt")
        sys.exit(1)
    vtt_to_words(sys.argv[1], sys.argv[2])
