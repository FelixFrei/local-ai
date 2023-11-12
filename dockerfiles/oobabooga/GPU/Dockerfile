# The source image to start with
FROM atinoda/text-generation-webui:latest
# Your contact info
MAINTAINER Felix Frei; felix.frei@gmx.ch

# Aktualisieren Sie die Paketliste und installieren Sie vim
RUN apt-get update && apt-get -y install vim wget

RUN mkdir -p '/opt/ai/'


# Setzen Sie das Arbeitsverzeichnis im Container
WORKDIR /opt/ai/

# Kopieren Sie die requirements.txt-Datei in das Arbeitsverzeichnis
COPY requirements.txt .

# Installieren Sie die Anwendungsabhängigkeiten
RUN pip install -r requirements.txt



# Erstellen Sie das Verzeichnis 'data/paul_graham/'
RUN mkdir -p 'data/swiss-football/'

WORKDIR /opt/ai/data/swiss-football

RUN wget 'https://org.football.ch/portaldata/28/Resources/Dokumente/DE/12_Schiedsrichterwesen/12_1_Weisungen_an_SR/12.1.1._Offizielle_Spielregeln_SFV-Praezisierungen.pdf'
RUN wget 'https://org.football.ch/portaldata/28/Resources/dokumente/de/12_schiedsrichterwesen/12_1_weisungen_an_sr/12.1.2._Zusammenfassung_spezieller_Spielregeln_2023_2024.pdf'
RUN wget 'https://org.football.ch/portaldata/28/Resources/dokumente/de/12_schiedsrichterwesen/12_1_weisungen_an_sr/12.1.3._Ausfuehrungsbestimmungen_Footeco_2023_2024.pdf'
RUN wget 'https://org.football.ch/portaldata/28/Resources/dokumente/de/12_schiedsrichterwesen/12_1_weisungen_an_sr/12.1.4_Administrative_Weisungen_2023_2024.pdf'
RUN wget 'https://org.football.ch/portaldata/28/Resources/Dokumente/DE/12_Schiedsrichterwesen/12_1_Weisungen_an_SR/12.1.5._Fussballturniere.pdf'
RUN wget 'https://org.football.ch/portaldata/28/Resources/dokumente/de/12_schiedsrichterwesen/12_1_weisungen_an_sr/12.1.6._Schiedsrichter-Entschaedigungen_2023_2024.pdf'
RUN wget 'https://org.football.ch/portaldata/28/Resources/Dokumente/DE/12_Schiedsrichterwesen/12_1_Weisungen_an_SR/12.1.7._Links.pdf'
RUN wget 'https://org.football.ch/portaldata/28/Resources/dokumente/de/12_schiedsrichterwesen/12_2_weiteres_material_fuer_sr/12.2.1._Regelaenderungen_IFAB.pdf'
RUN wget 'https://org.football.ch/portaldata/28/Resources/dokumente/de/12_schiedsrichterwesen/12_2_weiteres_material_fuer_sr/12.2.2._Regelaenderungen_2023_24.pdf'
RUN wget 'https://org.football.ch/portaldata/28/Resources/dokumente/de/12_schiedsrichterwesen/12_2_weiteres_material_fuer_sr/12.2.3._Richtlinien_zum_Stellungsspiel.pdf'
RUN wget 'https://org.football.ch/portaldata/28/Resources/dokumente/de/12_schiedsrichterwesen/12_2_weiteres_material_fuer_sr/12.2.5._Vorgehen_bei_Nichterscheinen.pdf'
RUN wget 'https://org.football.ch/portaldata/28/Resources/dokumente/de/12_schiedsrichterwesen/12_2_weiteres_material_fuer_sr/12.2.5._Vorgehen_bei_Nichterscheinen.pdf'
RUN wget 'https://org.football.ch/portaldata/28/Resources/dokumente/de/12_schiedsrichterwesen/12_2_weiteres_material_fuer_sr/12.2.6._Verhalten_bei_Protest.pdf'
RUN wget 'https://org.football.ch/portaldata/28/Resources/dokumente/de/12_schiedsrichterwesen/12_2_weiteres_material_fuer_sr/12.2.7._Protestformular_Formulaire_prot_t_Formulario_protesto.pdf'
RUN wget 'https://org.football.ch/portaldata/28/Resources/dokumente/de/12_schiedsrichterwesen/12_3_reglemente/12.3.1._Reglement_Schiedsrichter_Schiedsrichter-Assistenten.pdf'
RUN wget 'https://org.football.ch/portaldata/28/Resources/dokumente/de/12_schiedsrichterwesen/12_3_reglemente/12.3.2._Reglement_SR-Coaches.pdf'
RUN wget 'https://org.football.ch/portaldata/28/Resources/dokumente/de/12_schiedsrichterwesen/12_3_reglemente/12.3.3._Reglement_SR-Instruktoren.pdf'
RUN wget 'https://org.football.ch/portaldata/28/Resources/dokumente/de/12_schiedsrichterwesen/12_3_reglemente/12.3.4._Geschaeftsreglement__Schiedsrichterwesen.pdf'
RUN wget 'https://org.football.ch/portaldata/28/Resources/Dokumente/DE/12_Schiedsrichterwesen/12_4_Weisungen_an_die_reg_SK/12.4.1._Kurspflicht.pdf'
RUN wget 'https://org.football.ch/portaldata/28/Resources/Dokumente/DE/12_Schiedsrichterwesen/12_4_Weisungen_an_die_reg_SK/12.4.2._Einsatzkriterien.pdf'
RUN wget 'https://org.football.ch/portaldata/28/Resources/Dokumente/DE/12_Schiedsrichterwesen/12_4_Weisungen_an_die_reg_SK/12.4.3._Alterslimiten.pdf'
RUN wget 'https://org.football.ch/portaldata/28/Resources/Dokumente/DE/12_Schiedsrichterwesen/12_4_Weisungen_an_die_reg_SK/12.4.4._KO-Tests.pdf'
RUN wget 'https://org.football.ch/portaldata/28/Resources/Dokumente/DE/12_Schiedsrichterwesen/12_5_Ausbildungskonzept/12.5_SR-Ausbildungskonzept.pdf'
RUN wget 'https://org.football.ch/portaldata/28/Resources/dokumente/de/12_schiedsrichterwesen/12_6_organigramm/12.6_20230701_Organigram_SK_RD_D_F_I_ORIGINAL.pdf'
RUN wget 'https://org.football.ch/portaldata/28/Resources/dokumente/de/02_wettspielreglement_und_spielregeln/2.1_Wettspielreglement_Juli_2023.pdf'
RUN wget 'https://org.football.ch/portaldata/28/Resources/dokumente/de/02_wettspielreglement_und_spielregeln/2.2_Regelbuch_2023_2024_Deutsch.pdf'
RUN wget 'https://org.football.ch/portaldata/28/Resources/dokumente/de/02_wettspielreglement_und_spielregeln/Merkblatt_Gewitter_2022.pdf'
