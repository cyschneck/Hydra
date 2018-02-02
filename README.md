# BA CSCI Honors Thesis

Department of Computer Science at the University of Colorado, Boulder 2017-2018

The code in this repo is the working version of the thesis found in the link below. To run, follow instructions below

Link to final PDF (coming soon)

TODO: convert to Jupyter notebook

## Pre-Processing Text
Text is from Project Gutenberg and has been slightly modified for research purposes to run with the given scripts. This includes: removing Gutenberg UTF-8 header, chapter headings. For original text find at www.gutenberg.org

The raw text including for testing are both first and third person for benchmarking purposes:

Peter Pan (Barrie)

A Little Princess (Burnett)

Secret Garden (Burnett)

A Princess of Mars (Burroughs)

Alice’s Adventures in Wonderland (Carroll)

The Adventures of Sherlock Holmes (Doyle)

Fairy Tales (Grimm)

Legends of King Arthur and his Knights (Malory)

Le Morte d’Arthur v1 (Malory)

Le Morte d’Arthur v2 (Malory)

Moby Dick (Melville)

The Raven (Poe)

Frankenstein (Shelley)

The Strange Case of Dr. Jekyll and Mr. Hyde (Stevenson)

A Connecticut Yankee in King Arthur’s Court (Twain)

The Adventures of Tom Sawyer (Twain)

20,000 Leagues Under the Sea (Verne)

Around the World in Eighty Days (Verne)

Time Machine (Wells)

## Datasets
[Kaggle Names Corpus](https://www.kaggle.com/nltkdata/names/data "5001 female names and 2943 male")

## Install and Running SyntaxNet

The SyntaxNet documention contains a few errors. Some directory paths have changed.

Install bazel

Tensorflow requires bazel 0.4.5 or greater to run. Current version 0.10.0
```
wget https://github.com/bazelbuild/bazel/releases/download/0.10.0/bazel-0.10.0-installer-linux-x86_64.sh -O bazel-0.10.0-installer-linux-x86_64.sh
chmod +x bazel-0.10.0-installer-linux-x86_64.sh
sudo ./bazel-0.10.0-installer-linux-x86_64.sh --user
rm bazel-0.10.0-installer-linux-x86_64.sh
sudo chown $USER:$USER ~/.cache/bazel/
export PATH="$PATH:/home/user/bin"
```


## Citations
Names Corpus, Version 1.3 (1994-03-29)
Copyright (C) 1991 Mark Kantrowitz
Additions by Bill Ross

This corpus contains 5001 female names and 2943 male names, sorted
alphabetically, one per line.

You may use the lists of names for any purpose, so long as credit is
given in any published work. You may also redistribute the list if you
provide the recipients with a copy of this README file. The lists are
not in the public domain (I retain the copyright on the lists) but are
freely redistributable.  If you have any additions to the lists of
names, I would appreciate receiving them.

Mark Kantrowitz <mkant+@cs.cmu.edu>
http://www-2.cs.cmu.edu/afs/cs/project/ai-repository/ai/areas/nlp/corpora/names/
