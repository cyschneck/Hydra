#!/bin/bash
echo "install modules needed to run inside docker container..."
echo ""
sed -i -e 's/archive.ubuntu.com\|security.ubuntu.com/old-releases.ubuntu.com/g' /etc/apt/sources.list
apt-get update
echo 'y' | apt-get install vim

echo ""
echo "install nltk for tokens"
pip install nltk
echo -e "import nltk\nnltk.download('punkt')\nnltk.download('averaged_perceptron_tagger')" | python

echo "copying tagger for POS, replaced demo.sh"
cp /root/models/syntaxnet/Ishmael/pos_tagger.sh ~/models/syntaxnet/syntaxnet/
# To be commented out (for testing)
#echo "testing raw_text_processing.py is running"
#python raw_text_processing.py -F testing.txt 
