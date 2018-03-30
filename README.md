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
cd Hydra/
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
Text is from Project Gutenberg and has been slightly modified for research purposes to run with the given scripts. This includes: removing Gutenberg UTF-8 header and header information. For original text find at www.gutenberg.org

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

## Examples of Global Named Entities Found

Examples:

New York Mathematical Society (Time Machine)

Palace of Green Porcelain (Time Machine)

Royal Highness the Duke of Cumberland (Treasure Island)

Sign of the Spy-glass (Treasure Island)

Black Avenger of the Spanish Main (Tom Sawyer)

President of the United States (Tom Sawyer)

Captain Rollo Bickersteth of the Coldstream (My Man Jeeves)

Serene Highness the Prince of Saxburg-Leignitz (My Man Jeeves)

Rikk-tikk-tikki-tikki-tchk (The Jungle Book)

Toomai of the Elephants (The Jungle Book) 

Baloo of the Seeonee Wolf Pack (The Jungle Book)

Hunting People of the Jungle (The Jungle Book)

Dance of the Hunger of Kaa (The Jungle Book)

Bagheera of the Council Rock (The Jungle Book)

Superior of the Academy of the Presentation of the Blessed Virgin (Love in the Time of Cholera)

Assembly Chamber of the Provincial (Love in the Time of Cholera)

General Manager of the River Company of the Caribbean (Love in the Time of Cholera)

Knight of the Order of the Holy Sepulcher (Love in the Time of Cholera)

Waltz of the Crowned Goddess (Love in the Time of Cholera)

Director of the Astronomical Observatory (Love in the Time of Cholera)

Two Minutes Hate (1984)

Eleventh Edition of the Dictionary (1984)

Eleventh Edition of the Newspeak Dictionary (1984)

Order of Conspicuous Merit (1984)

Museum of the Faculty of Medicine of Paris (20,000 Leagues Under the Sea)

King of the Winged Monkeys (Wonderful Wizard of Oz)

Wicked Witch of the West (Wonderful Wizard of Oz)

Country of the Quadlings (Wonderful Wizard of Oz)

Sydney Cecil Vivian Montmorency (Little Princess)

Lilian Evangeline Maud Marion (Little Princess)


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

__Emma (Austen)__

IS FIRST PERSON TEXT: True

CHARACTER OF INTEREST: [('Emma Woodhouse', 963)]

ADDITIONAL TOP CHARACTERS OF INTEREST: [('Mr John Knightley', 663), ('Miss Harriet Smith', 568), ('Miss Jane Fairfax', 453), ('Mr Perry', 351), ('Mr Robert Martin', 327)]

__Pride and Prejudice (Austen)__

IS FIRST PERSON TEXT: False

Predicted gender of main character is 'Female' [('her', 2131)]: False

CHARACTER OF INTEREST: [('Mr Fitzwilliam Darcy', 522)]

ADDITIONAL TOP CHARACTERS OF INTEREST: [('Jane Bennet', 289), ('Lydia Wickham', 257), ('Mr Wickham', 183), ('Mrs Bennet', 158), ('George Wickham', 139)]


__Peter Pan (Barrie)__

IS FIRST PERSON TEXT: False

Predicted gender of main character is 'Male' [('he', 873)]: False

CHARACTER OF INTEREST: [('Wendy Moira Angela Darling', 322)]

ADDITIONAL TOP CHARACTERS OF INTEREST: [('Peter the Great White Father', 309), ('Captain Hook', 137), ('Johnny Corkscrew', 111), ('Michael', 96), ('Nana', 64)]

__The Wonderful Wizard of Oz (Baum)__

IS FIRST PERSON TEXT: True

CHARACTER OF INTEREST: [('Dorothy', 345)]

ADDITIONAL TOP CHARACTERS OF INTEREST: [('Wise Scarecrow', 224), ('Tin Woodman', 180), ('Cowardly Lion', 176), ('Wonderful City of Oz', 159), ('Wicked Witch of the West', 126)]

__A Little Princess (Burnett)__

IS FIRST PERSON TEXT: False

Predicted gender of main character is 'Female' [('she', 1685)]: False

CHARACTER OF INTEREST: [('Ermengarde St John', 149)]

ADDITIONAL TOP CHARACTERS OF INTEREST: [('Becky', 144), ('Lottie Legh', 60), ('Miss Amelia Minchin', 58), ('Emily', 56), ('Lavinia Herbert', 54)]

__Secret Garden (Burnett)__

IS FIRST PERSON TEXT: False

Predicted gender of main character is 'Male' [('he', 1365)]: False

CHARACTER OF INTEREST: [('Martha Phoebe Sowerby', 357)]

ADDITIONAL TOP CHARACTERS OF INTEREST: [('Mistress Mary Quite Contrary', 221), ('Master Colin', 109), ('Dickon', 84), ('Mrs Medlock', 44), ('Magic', 21)]

__Princess of Mars (Burroughs)__

IS FIRST PERSON TEXT: True

CHARACTER OF INTEREST: [('Princess Dejah Thoris', 172)]

ADDITIONAL TOP CHARACTERS OF INTEREST: [('Tars Tarkas the Thark', 132), ('Sola', 118), ('Tharks of Barsoom', 113), ('throng of Martians', 107), ('Mors Kajak of Helium', 104)]

__Tarzan of the Apes (Burroughs)__

IS FIRST PERSON TEXT: False

Predicted gender of main character is 'Male' [('he', 1493)]: True

CHARACTER OF INTEREST: [('Tarzan of the Dum-Dum', 604)]

ADDITIONAL TOP CHARACTERS OF INTEREST: [('Mr William Cecil Clayton', 293), ('Lieutenant Charpentier', 195), ('Jane Porter', 168), ('Mr Philander', 100), ('Professor Porter', 95)]

__Alices Adventures in Wonderland (Carroll)__

IS FIRST PERSON TEXT: False

Predicted gender of main character is 'Female' [('she', 492)]: True

CHARACTER OF INTEREST: [('Miss Alice', 370)]

ADDITIONAL TOP CHARACTERS OF INTEREST: [('Queen of Hearts', 73), ('Mock Turtle Soup', 62), ('Hatter', 55), ('Gryphon', 53), ('Rabbit Sends', 41)]

__Jaberwocky (Carroll)__

IS FIRST PERSON TEXT: False

Predicted gender of main character is 'Male' [('He', 4)]: True

CHARACTER OF INTEREST: [('Jabberwock', 4)]

ADDITIONAL TOP CHARACTERS OF INTEREST: [('Came', 1), ('Callooh', 1), ('Jubjub', 1), ('Tumtum', 1), ('Callay', 1)]

__The Mysterious Affair at Styles (Christie)__

IS FIRST PERSON TEXT: True

CHARACTER OF INTEREST: [('Monsieur Poirot', 374)]

ADDITIONAL TOP CHARACTERS OF INTEREST: [('Monsieur John Cavendish', 200), ('Murder of Emily Agnes Inglethorp', 162), ('Mr Hastings Miss Murdoch', 116), ('Mademoiselle Cynthia', 104), ('Mr Lawrence Cavendish', 74)]

__Heart of Darkness (Conrad)__

IS FIRST PERSON TEXT: True

CHARACTER OF INTEREST: [('Mistah Kurtz', 65)]

ADDITIONAL TOP CHARACTERS OF INTEREST: [('Mr Kurtz', 51), ('Company', 13), ('Charlie Marlow', 11), ('English', 10), ('Europe', 8)]

__A Christmas Carol (Dickens)__

IS FIRST PERSON TEXT: False

CHARACTER OF INTEREST: [('Scrooge the Baleful', 329)]

ADDITIONAL TOP CHARACTERS OF INTEREST: [('Ghost of Christmas Present', 174), ('Evil Spirit', 76), ('Bob Cratchit', 51), ('Tiny Tim', 22), ('Mrs Cratchit', 19)]

__A Tale of Two Cities (Dickens)__

IS FIRST PERSON TEXT: False

Predicted gender of main character is 'Male' [('his', 1940)]: True

CHARACTER OF INTEREST: [('Mr Jeremiah Cruncher', 180)]

ADDITIONAL TOP CHARACTERS OF INTEREST: [('Mr Charles Darnay', 168), ('Citizeness Defarge', 148), ('Madame Defarge', 125), ('Miss Pross', 109), ('Monsieur the Marquis', 109)]

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

__The Scarlet Letter (Hawthorne)__

IS FIRST PERSON TEXT: False

Predicted gender of main character is 'Female' [('her', 934)]: False

CHARACTER OF INTEREST: ('Interpreting Hester Prynne', 359)

TOP CHARACTERS OF INTEREST: [('Little Pearl', 194), ('Reverend Mr Dimmesdale', 94), ('Old Roger Chillingworth', 70), ('Salem Custom-House', 36)]

__Metamorphosis (Kafka)__

IS FIRST PERSON TEXT: False

Predicted gender of main character is 'Male' [('his', 524)]: True

CHARACTER OF INTEREST: ('Gregor Samsa', 292)

TOP CHARACTERS OF INTEREST: [('Grete', 25), ('Mr Samsa', 21), ('Mrs Samsa', 10), ('Mother', 4)]

__The Trial (Kafka)__

IS FIRST PERSON TEXT: False

Predicted gender of main character is 'Male' [('he', 1699)]: False

CHARACTER OF INTEREST: ('Leni', 93)

TOP CHARACTERS OF INTEREST: [('Then Miss B rstner', 73), ('No', 59), ('Alright Block', 57), ('Mrs Grubach', 52)]

__The Jungle Book (Kipling)__

IS FIRST PERSON TEXT: False

Predicted gender of main character is 'Male' [('he', 865)]: True

CHARACTER OF INTEREST: ('Song of Mowgli', 206)

TOP CHARACTERS OF INTEREST: [('Bagheera of the Council Rock', 151), ('Tell Baloo of the Seeonee Pack', 132), ('O Kala Nag', 98), ('Valiant Rikki-tikki', 95)]

__The Call of the Wild (London)__

IS FIRST PERSON TEXT: False

Predicted gender of main character is 'Male' [('he', 616)]: True

CHARACTER OF INTEREST: ('Fang Buck', 351)

TOP CHARACTERS OF INTEREST: [('John Thornton', 102), ('Spitzbergen', 60), ('Francois', 60), ('Perrault', 39)]

__White Fang (London)__

IS FIRST PERSON TEXT: False

Predicted gender of main character is 'Male' [('he', 1531)]: True

CHARACTER OF INTEREST: ('SOUTHLAND White Fang', 598)

TOP CHARACTERS OF INTEREST: [('Grey Beaver', 119), ('Henry', 95), ('DEATH Beauty Smith', 84), ('Matt', 82)]

__Love in the Time of Cholera (Marquez)__

IS FIRST PERSON TEXT: False

Predicted gender of main character is 'Male' [('he', 2921)]: False

CHARACTER OF INTEREST: ('Doha Fermina Daza', 409)

TOP CHARACTERS OF INTEREST: [('Dr Marco Aurelio Urbino Daza', 174), ('Dr Juvenal Urbino', 92), ('Captain Diego Samaritano', 60), ('Doctor of Theology', 46)]

__1984 (Orwell)__

IS FIRST PERSON TEXT: False

CHARACTER OF INTEREST: ('Emmanuel Goldstein Winston', 493)

TOP CHARACTERS OF INTEREST: [('Labour Party', 213), ("O'Brien Julia", 188), ('Eleventh Edition of the Newspeak Dictionary', 71), ('Government of Oceania', 59)]
 
__Raven (Poe)__

IS FIRST PERSON TEXT: True

CHARACTER OF INTEREST: ('Quoth the Raven', 10)

TOP CHARACTERS OF INTEREST: [('Lenore', 8), ('Nevermore', 8), ('Perched', 2), ('December', 2)]

__The Merry Adventures of Robin Hood (Pyle)__

IS FIRST PERSON TEXT: False

Predicted gender of main character is 'Male' [('he', 1913)]: True

CHARACTER OF INTEREST: ('Epilogue THUS END the Merry Adventures of Robin Hood', 691)

TOP CHARACTERS OF INTEREST: [('Quoth the Sheriff of Nottingham', 351), ('quoth Robin Hood', 342), ('Little John thereupon', 335), ('stout William of the Scar', 192)]

__Frankenstein (Shelley)__

IS FIRST PERSON TEXT: True

CHARACTER OF INTEREST: ('Elizabeth Lavenza', 89)

TOP CHARACTERS OF INTEREST: [('Justine Moritz', 54), ('Dearest Clerval', 49), ('Felix', 48), ('Geneva', 36)]

__The Strange Case of Dr. Jekyll and Mr. Hyde (Stevenson)__

IS FIRST PERSON TEXT: True

CHARACTER OF INTEREST: ('Mr Utterson of Gaunt Street', 125)

TOP CHARACTERS OF INTEREST: [('Edward Hyde', 65), ('Poole', 58), ('Poor Harry Jekyll', 45), ('Mr Hyde', 30)]

__Tresure Island (Stevenson)__

IS FIRST PERSON TEXT: True

CHARACTER OF INTEREST: ('Long John Silver', 232)

TOP CHARACTERS OF INTEREST: [('Jim Hawkins', 96), ('Captain Flint', 50), ('Dr Livesey', 47), ('John Trelawney Postscript', 47)]

__20,000 Leagues Under the Sea (Verne)__

IS FIRST PERSON TEXT: True

CHARACTER OF INTEREST: ('To-morrow Captain Nemo', 283)

TOP CHARACTERS OF INTEREST: [('Commander of the Nautilus', 195), ('Happily Conseil', 193), ('Canadian', 144), ('Captain Denham of the Herald', 126)]

__Around the World in Eighty Days (Verne)__

IS FIRST PERSON TEXT: False

Predicted gender of main character is 'Male' [('his', 807)]: True

CHARACTER OF INTEREST: ('Passepartout thereupon', 357)

TOP CHARACTERS OF INTEREST: [('Dear Mr Fogg', 339), ('HAPPINESS Yes Phileas Fogg', 231), ('Monsieur Fix', 227), ('abandon Aouda', 127)]

__The Island of Doctor Moreau (Wells)__

IS FIRST PERSON TEXT: True

CHARACTER OF INTEREST: ('Montgomery', 202)

TOP CHARACTERS OF INTEREST: [('Island of Doctor Moreau', 134), ('Sayer of the Law', 61), ('Beast People', 45), ("M'ling", 40)]

__The War of the Worlds (Wells)__

IS FIRST PERSON TEXT: True

CHARACTER OF INTEREST: ('Repulse of the Martians', 81)

TOP CHARACTERS OF INTEREST: [('Pool of London', 46), ('Old Woking', 43), ('Heat-Ray', 27), ('Mars', 24)]

__Time Machine (Wells)__

IS FIRST PERSON TEXT: True

CHARACTER OF INTEREST: ('Time Traveller', 67)

TOP CHARACTERS OF INTEREST: [("'Little Weena", 48), ('Time Machine', 33), ("Medical Man 'but", 23), ('Psychologist', 22)]

__My Man Jeeves (Wodehouse)__

IS FIRST PERSON TEXT: True

CHARACTER OF INTEREST: ('Jeeves', 229)

TOP CHARACTERS OF INTEREST: [('Mr George Lattaker', 94), ('Rocky Todd', 60), ('Old Bicky', 56), ('Bobbie Cardew', 56)]

## Additional Citations

[Kaggle Names Corpus](https://www.kaggle.com/nltkdata/names/data "5001 female names and 2943 male")

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
