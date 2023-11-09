# The source image to start with
FROM atinoda/text-generation-webui:latest
# Your contact info
MAINTAINER Felix Frei; felix.frei@gmx.ch

# Aktualisieren Sie die Paketliste und installieren Sie vim
RUN apt-get update && apt-get -y install vim wget

# Setzen Sie das Arbeitsverzeichnis im Container
WORKDIR /app

# Kopieren Sie die requirements.txt-Datei in das Arbeitsverzeichnis
COPY requirements.txt .

# Installieren Sie die Anwendungsabhängigkeiten
RUN pip install -r requirements.txt


# Erstellen Sie das Verzeichnis 'data/paul_graham/'
RUN mkdir -p 'data/paul_graham/'


RUN wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt'
