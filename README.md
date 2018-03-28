# Hydra

Department of Computer Science at the University of Colorado, Boulder

The code in this repo is the working version of the thesis found in the link below. To run, follow instructions below

Link to final PDF (coming soon)

## Install and Run
```git clone https://github.com/cschneck/Hydra.git```

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

![all_nouns_all_words](https://github.com/cschneck/Hydra/blob/master/plot_percent_data/all_nouns_in_all_words.png)
![pronouns_all_words](https://github.com/cschneck/Hydra/blob/master/plot_percent_data/pronouns_in_all_words.png)
![proper_nouns_all_nouns](https://github.com/cschneck/Hydra/blob/master/plot_percent_data/proper_nouns_in_all_nouns.png)
![regular_nouns_all_nouns](https://github.com/cschneck/Hydra/blob/master/plot_percent_data/regular_nouns_in_all_nouns.png)

## Tagging text for Pronouns and Proper nouns

```One morning, when <Gregor Samsa>_n0 woke from troubled dreams, <he>_p0 found <himself>_p1 transformed in <his>_p2 bed into a horrible vermin. <He>_p3 lay on <his>_p4 armour-like back,  and if <he>_p7 lifted <his>_p5 head a little <he>_p8 could see <his>_p5 brown belly,  slightly domed and divided by arches into stiff sections. The bedding was hardly able to cover <it>_p9 and seemed ready to slide off any moment. <His>_p10 many legs,  pitifully thin compared with the size of the rest of <him>_p11,  waved about helplessly as <he>_p12 looked.```

```<Scarlett O'Hara>_n0 was not beautiful, but men seldom realized <it>_p0 when caught by <her>_p1 charm as the <Tarleton>_n1 twins were. In <her>_p2 face were too sharply blended the delicate features of <her>_p3 mother, a <Coast>_n2 aristocrat of French descent, and the heavy ones of <her>_p3 florid Irish father.```


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

Alice’s Adventures in Wonderland (Carroll)

The Mysterious Affair at Styles (Christie)

Heart of Darkness (Conrad)

The Life and Adventures of Robinson Cruseo (Defoe)

A Christmas Carol in Prose (Dickens)

A Tale of Two Cities (Dickens)

The Great Expectation (Dickens)

Narrative of the Life of Frederick Douglass (Douglass)

The Adventures of Sherlock Holmes (Doyle)

The Hound of the Baskervilles (Doyle)

The Sign of Four (Doyle)

The Scarlet Letter (Hawthorne)

Metamorphosis (Kafka)

The Trial (Kafka)

The Jungle Book (Kipling)

The Call of the Wild (London)

White Fang (London)

Legends of King Arthur and his Knights (Malory)

Le Morte d’Arthur v1 (Malory)

Le Morte d’Arthur v2 (Malory)

Love in the Time of Cholera (Marquez)

Moby Dick (Melville)

1984 (Orwell)

The Raven (Poe)

The Merry Adventures of Robin Hood (Pyle)

Frankenstein (Shelley)

The Jungle (Sinclair)

The Strange Case of Dr. Jekyll and Mr. Hyde (Stevenson)

Treasure Island (Stevenson)

Dracula (Stoker)

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

## Examples of Long Global Named Entities Found

Examples:

New York Mathematical Society (Time Machine)

Palace of Green Porcelain (Time Machine)

Royal Highness the Duke of Cumberland (Treasure Island)

Sign of the Spy-glass (Treasure Island)

Black Avenger of the Spanish Main (Tom Sawyer)

President of the United States (Tom Sawyer)

Captain Rollo Bickersteth of the Coldstream (My Man Jeeves)

Serene Highness the Prince of Saxburg-Leignitz (My Man Jeeves)

## Gender Name Classifier (DecisionTreeClassifier)

The name 'Atticus' is most likely Male

Odds: Female (0.215384615385), Male (0.784615384615)


The name 'Emma' is most likely Female

Odds: Female (0.9), Male (0.1)


The name 'Taako' is most likely Male

Odds: Female (0.462962962963), Male (0.537037037037)


The name 'Ishamel' is most likely Male

Odds: Female (0.4), Male (0.6)


## Identify Main Character and Perspective of Text

__Pride and Prejudice (Austen)__
IS FIRST PERSON TEXT: False

Predicted gender of main character is 'Female' [('her', 2132)]: True

CHARACTER OF INTEREST: ('Miss Jane Bennet', 290)

TOP CHARACTERS OF INTEREST: [('Mr Darcy', 215), ('Mrs Bennet', 153), ('Mr Fitzwilliam Darcy', 153), ('Miss Lydia Bennet', 135)]

__Peter Pan (Barrie)__

IS FIRST PERSON TEXT: False

Predicted gender of main character is 'Male' [('he', 873)]: True

CHARACTER OF INTEREST: ('Peter the Great White Father', 373)

TOP CHARACTERS OF INTEREST: [('Wendy Moira Angela Darling', 354), ('Captain Hook', 155), ('Johnny Corkscrew', 136), ('Michael', 109)]

__The Wonderful Wizard of Oz (Baum)__

IS FIRST PERSON TEXT: True

CHARACTER OF INTEREST: ('Good Witch Grants Dorothy', 386)

TOP CHARACTERS OF INTEREST: [('Wise Scarecrow', 224), ('Rescue of the Tin Woodman', 177), ('Cowardly Lion', 175), ('Wonderful City of Oz', 137)]

__A Little Princess (Burnett)__

IS FIRST PERSON TEXT: False

Predicted gender of main character is 'Female' [('she', 1685)]: True

CHARACTER OF INTEREST: ('Miss Minchin', 244)

TOP CHARACTERS OF INTEREST: [('Miss Ermengarde', 147), ('Becky', 142), ('Lottie Lavinia', 57), ('Emily', 56)]

__Princess of Mars (Burroughs)__

IS FIRST PERSON TEXT: True

CHARACTER OF INTEREST: ('Princess Dejah Thoris', 173)

TOP CHARACTERS OF INTEREST: [('Tars Tarkas the Thark', 129), ('DOG Sola', 117), ('Tharks of Barsoom', 113), ('throng of Martians', 104)]

__Tarzan of the Apes (Burroughs)__

IS FIRST PERSON TEXT: False

Predicted gender of main character is 'Male' [('he', 1493)]: True

CHARACTER OF INTEREST: ('Tarzan of the Dum-Dum', 596)

TOP CHARACTERS OF INTEREST: [('Mr William Cecil Clayton', 239), ("Lieutenant D'Arnot", 173), ('Jane Porter', 163), ('Mr Philander', 98)]

__Alices Adventures in Wonderland (Carroll)__

IS FIRST PERSON TEXT: False

Predicted gender of main character is 'Female' [('she', 492)]: True

CHARACTER OF INTEREST: ('Rabbit-Hole Alice', 370)

TOP CHARACTERS OF INTEREST: [('Queen of Hearts', 69), ('King', 61), ('Mock Turtle Soup', 59), ('Hatter', 55)]

__The Mysterious Affair at Styles (Christie)__

IS FIRST PERSON TEXT: True

CHARACTER OF INTEREST: ('Show Monsieur Poirot', 370)

TOP CHARACTERS OF INTEREST: [('Monsieur John Cavendish', 194), ('Monday Mrs Inglethorp', 127), ('Mademoiselle Cynthia', 97), ('Mr Hastings Miss Howard', 82)]

__Heart of Darkness (Conrad)__

IS FIRST PERSON TEXT: True

CHARACTER OF INTEREST: ('Mistah Kurtz', 65)

TOP CHARACTERS OF INTEREST: [('Mr Kurtz', 51), ('Company', 13), ('Charlie Marlow', 11), ('English', 10)]

__A Christmas Carol (Dickens)__

IS FIRST PERSON TEXT: False

CHARACTER OF INTEREST: ('Scrooge the Baleful', 323)

TOP CHARACTERS OF INTEREST: [('Ghost of Christmas Present', 128), ('Evil Spirit', 79), ('Bob Cratchit', 49), ('Ghost of Jacob Marley', 37)]

__A Tale of Two Cities (Dickens)__

IS FIRST PERSON TEXT: False

Predicted gender of main character is 'Male' [('his', 1941)]: False

CHARACTER OF INTEREST: ('Citizeness Defarge', 148)

TOP CHARACTERS OF INTEREST: [('Storm Doctor Manette', 146), ('Madame Defarge', 125), ('Mr Charles Darnay', 119), ('Miss Pross', 105)]

__Great Expectations (Dickens)__

IS FIRST PERSON TEXT: True

CHARACTER OF INTEREST: ('Mrs Joe Gargery', 612)

TOP CHARACTERS OF INTEREST: [('Estella Miss Havisham', 536), ('Identity of Mr Pip', 255), ('Memorandum of Herbert', 240), ('Dear Biddy', 230)]

__Sherlock Holmes (Doyle)__

IS FIRST PERSON TEXT: True

CHARACTER OF INTEREST: ('Mister Sherlock Holmes', 342)

TOP CHARACTERS OF INTEREST: [('Dr Watson', 75), ('Mr Holmes', 67), ('Mr Lestrade of Scotland Yard', 42), ('City of London', 41)]

__The Hound of the Baskervillies (Doyle)__

IS FIRST PERSON TEXT: True

CHARACTER OF INTEREST: ('Baskerville Hall Sir Henry Baskerville', 233)

TOP CHARACTERS OF INTEREST: [('Mr Sherlock Holmes Mr Sherlock Holmes', 161), ('Second Report of Dr Watson', 110), ('Sir Charles Baskerville', 93), ('Dr Mortimer', 68)]

__Time Machine (Wells)__

IS FIRST PERSON TEXT: True

CHARACTER OF INTEREST: ('Time Traveller', 67)

TOP CHARACTERS OF INTEREST: [("'Little Weena", 48), ('Time Machine', 33), ("Medical Man 'but", 23), ('Psychologist', 22)]

__Treasure Island (Stevenson)__

IS FIRST PERSON TEXT: True

CHARACTER OF INTEREST: ('Long John Silver', 232)

TOP CHARACTERS OF INTEREST: [('Jim Hawkins', 96), ('Captain Flint', 50), ('Dr Livesey', 47), ('John Trelawney Postscript', 47)]

__The Strange Case of Dr. Jekyll and Mr. Hyde (Stevenson)__

IS FIRST PERSON TEXT: True
CHARACTER OF INTEREST: ('Mr Utterson of Gaunt Street', 125)

TOP CHARACTERS OF INTEREST: [('Edward Hyde', 65), ('Poole', 58), ('Poor Harry Jekyll', 45), ('Mr Hyde', 30)]

__Dracula (Stoker)__

__My Man Jeeves (Wodehouse)__

IS FIRST PERSON TEXT: True

CHARACTER OF INTEREST: ('Jeeves', 229)

TOP CHARACTERS OF INTEREST: [('Mr George Lattaker', 94), ('Rocky Todd', 60), ('Old Bicky', 56), ('Bobbie Cardew', 56)]



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
