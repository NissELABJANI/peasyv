# Utiliser l'image x86_64 pour compatibilité 32 bits
FROM --platform=linux/amd64 python:3.12-bullseye

# Ajouter la prise en charge 32 bits et installer les dépendances système
RUN dpkg --add-architecture i386 && \
    apt-get update && \
    apt-get install -y \
        build-essential \
        gcc-multilib \
        libc6-dev-i386 \
        libx11-dev:i386 \
        sox \
        wget \
        git \
        ffmpeg \
        curl \
        unzip \
        vim \
        python3-pip \
        python3-venv && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers du projet
COPY . /app

# Installer les dépendances Python
RUN pip install --no-cache-dir flask webvtt-py nltk

# Télécharger les données NLTK
RUN python3 -m nltk.downloader punkt

# Installer yt-dlp
RUN pip install yt-dlp


# Compilation de HTK
RUN tar -xvzf HTK-3.4.tar.gz -C /tmp && \
    cd /tmp/htk && \
    export CPPFLAGS=-UPHNALG && \
    ./configure --disable-hlmtools --disable-hslab && \
    make -j4 all && \
    make install

# Exposer le port 5000
EXPOSE 5000

# Lancer l'application Flask
CMD ["python3", "app.py"]
