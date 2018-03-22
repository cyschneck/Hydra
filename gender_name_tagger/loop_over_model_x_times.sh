#!/bin/bash
# run model in background 100 times to attempt to find more accurate model (~84%)

for i in {1..100}; do
    python NN_gender_class.py
done
