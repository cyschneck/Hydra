#!/bin/bash
# run model in background 100 times

for i in {1..100}; do
    python NN_gender_class.py
done
