#!/bin/bash
# run raw_text parser pre-processing for all text files automatically in order rather than manually to populate dataset
for text_file in `ls Raw_Text/ | grep -v README`
do 
    echo "Running pre-processing shell script to activate parser on $text_file"
    python raw_text_processing.py -F Raw_Text/$text_file
    echo ""
done
