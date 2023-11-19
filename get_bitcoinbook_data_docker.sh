# Setup bitcoinbook data

# Install the required packages


git clone https://github.com/bitcoinbook/bitcoinbook.git

cd bitcoinbook

# Create the output directory
mkdir -p ../data/bitcoinbook

# Convert all AsciiDoc files to PDF and copy them to the output directory
for file in *.asciidoc; do
 asciidoctor-pdf "$file"
done

cp *.pdf ../data/bitcoinbook
