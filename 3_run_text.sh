#!/bin/bash
ECHO_COMMAND=$1 

cd /root/models/syntaxnet/Ishmael

# return CoNLL table
cd /root/models/syntaxnet/ && echo $ECHO_COMMAND | ~/models/syntaxnet/syntaxnet/pos_tagger.sh && cd Ishmael/

# return ascii tree
cd /root/models/syntaxnet/ && echo $ECHO_COMMAND | ~/models/syntaxnet/syntaxnet/demo.sh && cd Ishmael/
