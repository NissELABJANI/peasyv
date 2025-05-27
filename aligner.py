import sys
import subprocess
import os

def align(wav_path, txt_path, output_path):
    if not os.path.exists("p2fa/align.py"):
        print("Erreur : align.py de P2FA introuvable.")
        sys.exit(1)

    try:
        subprocess.run([
            "python3", "p2fa/align.py", wav_path, txt_path, output_path
        ], check=True)
        print("Alignement terminé :", output_path)
    except subprocess.CalledProcessError as e:
        print("Erreur lors de l'alignement :", e)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 aligner.py fichier.wav fichier.txt sortie.TextGrid")
        sys.exit(1)

    wav_file = sys.argv[1]
    txt_file = sys.argv[2]
    output_file = sys.argv[3]

    align(wav_file, txt_file, output_file)
