#!/bin/bash
ECHO_COMMAND=$1 

cd /root/models/syntaxnet/Ishmael

# return CoNLL table, output std to /dev/null
cd /root/models/syntaxnet/ && echo $ECHO_COMMAND | ~/models/syntaxnet/syntaxnet/pos_tagger.sh  2> /dev/null
cd Ishmael/

# return ascii tree, output std to /dev/null
#cd /root/models/syntaxnet/ && echo $ECHO_COMMAND | ~/models/syntaxnet/syntaxnet/demo.sh 2> /dev/null
#cd Ishmael/
