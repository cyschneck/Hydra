# Ishmael

Department of Computer Science at the University of Colorado, Boulder

The code in this repo is the working version of the thesis found in the link below. To run, follow instructions below

Link to final PDF (coming soon)

TODO: update GNE for most common surrouding elements, create global name as the shared elements of GNES, research pronoun features (binding theory), generate percentNouns graphs, label pronouns (gender, plurality), cut off counter based on the size of the given text, manual labeling, accuracy test

## Install and Run
```git clone https://github.com/cschneck/Ishmael.git```

1. If first time setup:

```./0_first_time_install.sh ```

This script will install all docker related modules to enable the next steps

2. To run docker image within repo, starts docker:

```./1_start_docker.sh```
```
Linking repo volumne inside of syntaxnet docker container

DOCKER STARTING, entering docker...
```

2. Install modules within docker to run repo (will take a few minutes):

```
cd Ishmael/
./2_install_modules_in_docker.sh
```
```
install modules needed to run inside docker container...

Get:1 http://old-releases.ubuntu.com wily InRelease [218 kB]
Get:2 http://old-releases.ubuntu.com wily-updates InRelease [65.9 kB]
...
```
The script is now ready to run

3. Run parser on text:

```python raw_text_processing.py -F <filename>.txt```

Example: Test parser with string

```./3_run_text.sh "Very well, I will marry you if you promise not to make me eat eggplant"```


## Parser output
CoNLL

![image](https://user-images.githubusercontent.com/22159116/36015676-b48e83ac-0d2c-11e8-9241-03c0b88e1bd5.png)

ASCII tree

![image](https://user-images.githubusercontent.com/22159116/36015691-d2ef764e-0d2c-11e8-9702-72254ffb8c42.png)

Will only run the parser once, if the parser has been run already, the output will be stored in the csv file for future use

## Part of Speech Data

![all_nouns_all_words](https://github.com/cschneck/Ishmael/blob/master/plot_percent_data/all_nouns_in_all_words.png)
![pronouns_all_words](https://github.com/cschneck/Ishmael/blob/master/plot_percent_data/pronouns_in_all_words.png)
![proper_nouns_all_nouns](https://github.com/cschneck/Ishmael/blob/master/plot_percent_data/proper_nouns_in_all_nouns.png)
![regular_nouns_all_nouns](https://github.com/cschneck/Ishmael/blob/master/plot_percent_data/regular_nouns_in_all_nouns.png)

## Tagging text for Pronouns and Proper nouns

```One morning, when [Gregor Samsa]_n0 woke from troubled dreams, [he]_p0 found [himself]_p1 transformed in [his]_p2 bed into a horrible vermin. [He]_p3 lay on [his]_p4 armour-like back, and if [he]_p7 lifted [his]_p5 head a little [he]_p8 could see [his]_p5 brown belly, slightly domed and divided by arches into stiff sections. The bedding was hardly able to cover [it]_p9 and seemed ready to slide off any moment. [His]_p10 many legs, pitifully thin compared with the size of the rest of him, waved about helplessly as [he]_p11 looked.```


## Pre-Processing Text
Text is from Project Gutenberg and has been slightly modified for research purposes to run with the given scripts. This includes: removing Gutenberg UTF-8 header, chapter headings. For original text find at www.gutenberg.org

The raw text including for testing are both first and third person for benchmarking purposes:

Emma (Austen)

Pride and Prejudice (Austen)

Peter Pan (Barrie)

The Wonderful Wizard of Oz (Baum)

Jane Eyre (Bronte)

A Little Princess (Burnett)

Secret Garden (Burnett)

A Princess of Mars (Burroughs)

Tarzan of the Apes (Burroughs)

The Book of a Thousand Nights and a Night (Burton)

Alice’s Adventures in Wonderland (Carroll)

The Mysterious Affair at Styles (Christie)

Heart of Darkness (Conrad)

On the Origin of Species by Means of Natural Selection (Darwin)

The Voyage of the Beagle (Darwin)

The Life and Adventures of Robinson Cruseo (Defoe)

A Christmas Carol in Prose (Dickens)

A Tale of Two Cities (Dickens)

The Great Expectation (Dickens)

Narrative of the Life of Frederick Douglass (Douglass)

The Adventures of Sherlock Holmes (Doyle)

The Hound of the Baskervilles (Doyle)

The Sign of Four (Doyle)

The Man in the Iron Mask (Dumas)

Autobiography of Benjamin Franklin (Franklin)

The Federalist Papers (Hamliton/Jay/Madison)

The Scarlet Letter (Hawthorne)

The Trial (Kafka)

The Jungle Book (Kipling)

The Call of the Wild (London)

White Fang (London)

Legends of King Arthur and his Knights (Malory)

Le Morte d’Arthur v1 (Malory)

Le Morte d’Arthur v2 (Malory)

Moby Dick (Melville)

The Raven (Poe)

The Merry Adventures of Robin Hood (Pyle)

Frankenstein (Shelley)

The Jungle (Sinclair)

The Strange Case of Dr. Jekyll and Mr. Hyde (Stevenson)

Treasure Island (Stevenson)

Dracula (Stoker)

Anna Karenina (Tolstoy)

A Connecticut Yankee in King Arthur’s Court (Twain)

The Adventures of Tom Sawyer (Twain)

The Prince and the Pauper (Twain)

20,000 Leagues Under the Sea (Verne)

Around the World in Eighty Days (Verne)

The Island of Doctor Moreau (Wells)

The War of the Worlds (Wells)

The Time Machine (Wells)

The Picture of Dorian Gray (Wells)

My Man Jeeves (Wodehouse)


## Datasets
[Kaggle Names Corpus](https://www.kaggle.com/nltkdata/names/data "5001 female names and 2943 male")

## Benchmarking

[Feuding Families and Former Friends: Unsupervised Learning for Dynamic Fictional Relationships](https://www.cs.umd.edu/~miyyer/pubs/2016_naacl_relationships.pdf)

Code from paper found [here](https://github.com/miyyer/rmn)

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
