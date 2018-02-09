#!/bin/bash
ECHO_COMMAND=$1 

cd /root/models/syntaxnet/Ishmael
cd /root/models/syntaxnet/ && echo $ECHO_COMMAND | ~/models/syntaxnet/syntaxnet/pos_tagger.sh && cd Ishmael/

