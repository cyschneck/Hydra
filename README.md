# Hydra

Department of Computer Science at the University of Colorado, Boulder

The code in this repo is the working version of the thesis found in the link below. To run, follow instructions below

[Final Undergraduate Honors Thesis - **Hail Hydra: Named Entity Resolution, Extraction, and Linking of Lexically Similar Names**](https://scholar.colorado.edu/honr_theses/1566/)

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

Runtime for Parsey
![runtime_parsey](https://github.com/cschneck/Hydra/blob/master/plot_percent_data/runtime_parsey_data.png)

## Part of Speech Data


| ![all_nouns_all_words](https://github.com/cschneck/Hydra/blob/master/plot_percent_data/all_nouns_in_all_words.png) | ![pronouns_all_words](https://github.com/cschneck/Hydra/blob/master/plot_percent_data/pronouns_in_all_words.png) |
| ------------- | ------------- |
| ![proper_nouns_all_nouns](https://github.com/cschneck/Hydra/blob/master/plot_percent_data/proper_nouns_in_all_nouns.png) | ![regular_nouns_all_nouns](https://github.com/cschneck/Hydra/blob/master/plot_percent_data/regular_nouns_in_all_nouns.png) |
| ![gne_all_words](https://github.com/cschneck/Hydra/blob/master/plot_percent_data/gnes_in_all_words.png) | ![gne_all_nouns](https://github.com/cschneck/Hydra/blob/master/plot_percent_data/gnes_in_all_nouns.png) |

## Tagging text for Pronouns and Proper nouns

```One morning, when <Gregor Samsa>_n0 woke from troubled dreams, <he>_p0 found <himself>_p1 transformed in <his>_p2 bed into a horrible vermin. <He>_p3 lay on <his>_p4 armour-like back,  and if <he>_p7 lifted <his>_p5 head a little <he>_p8 could see <his>_p5 brown belly,  slightly domed and divided by arches into stiff sections. The bedding was hardly able to cover <it>_p9 and seemed ready to slide off any moment. <His>_p10 many legs,  pitifully thin compared with the size of the rest of <him>_p11,  waved about helplessly as <he>_p12 looked.```

```<Scarlett O'Hara>_n0 was not beautiful, but men seldom realized <it>_p0 when caught by <her>_p1 charm as the <Tarleton>_n1 twins were. In <her>_p2 face were too sharply blended the delicate features of <her>_p3 mother, a <Coast>_n2 aristocrat of French descent, and the heavy ones of <her>_p3 florid Irish father.```

## Network Interactions

Further examples found in [/network_interactions](https://github.com/cyschneck/Hydra/tree/master/network_interactions)

**Legend:**

Green Node - Female Named Entity

Purple Node - Male Named Entity

Blue Link - Negative Interaction (sadness, loss, etc...)

Red Link - Postive Interaction (passion, hatred, love, etc..)

__The Wonderful Wizard of Oz (Baum)__

![wonderful_wizard_network_interactions](https://github.com/cyschneck/Hydra/blob/master/network_interactions/BAUM_THE_WONDERFUL_WIZARD_OF_OZ_NETWORK_INTERACTIONS.gv.png)

__The Secret Garden (Burnett)__

![secret_garden_network_interactions](https://github.com/cyschneck/Hydra/blob/master/network_interactions/BURNETT_SECRET_GARDEN_NETWORK_INTERACTIONS.gv.png)

__Metamorphosis (Kafka)__
![metamorphosis_network_interactions](https://github.com/cyschneck/Hydra/blob/master/network_interactions/KAFKA_METAMORPHOSIS_NETWORK_INTERACTIONS.gv.png)


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

Jabberwocky (Carroll)

The Mysterious Affair at Styles (Christie)

Heart of Darkness (Conrad)

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

1984 (Orwell)

The Raven (Poe)

Frankenstein (Shelley)

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

Principal of the Theological College of St George (Sherlock Holmes)

League of the Red-headed Men (Sherlock Holmes)

Wilhelm Gottsreich Sigismond von Ormstein (Sherlock Holmes)


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

CHARACTER OF INTEREST: [('Emma Woodhouse', 821)]

ADDITIONAL TOP CHARACTERS OF INTEREST: [('Miss Harriet Smith', 437), ('Mr John Knightley', 355), ('Miss Jane Fairfax', 313), ('Weston Churchill', 251), ('Miss Woodhouse of Hartfield', 129)]

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

Predicted gender of main character is 'Female' [('she', 1685)]: True

CHARACTER OF INTEREST: [('Miss Amelia Minchin', 249)]

ADDITIONAL TOP CHARACTERS OF INTEREST: [('Ermengarde St John', 149), ('Becky', 145), ('Lottie Legh', 61), ('Emily', 56), ('Lavinia Herbert', 54)]

__Secret Garden (Burnett)__

IS FIRST PERSON TEXT: False

Predicted gender of main character is 'Male' [('he', 1365)]: False

CHARACTER OF INTEREST: [('Mistress Mary Quite Contrary', 669)]

ADDITIONAL TOP CHARACTERS OF INTEREST: [('Martha Phoebe Sowerby', 481), ('Dickon', 221), ('Mrs Medlock', 130), ('Ben Weatherstaff', 112), ('Master Colin', 111)]

__Princess of Mars (Burroughs)__

IS FIRST PERSON TEXT: True

CHARACTER OF INTEREST: [('Princess Dejah Thoris', 171)]

ADDITIONAL TOP CHARACTERS OF INTEREST: [('Tars Tarkas the Thark', 132), ('Sola', 118), ('Tharks of Barsoom', 113), ('throng of Martians', 107), ('Mors Kajak of Helium', 104)]

__Tarzan of the Apes (Burroughs)__

IS FIRST PERSON TEXT: False

Predicted gender of main character is 'Male' [('he', 1493)]: True

CHARACTER OF INTEREST: [('Tarzan of the Dum-Dum', 604)]

ADDITIONAL TOP CHARACTERS OF INTEREST: [('Mr William Cecil Clayton', 286), ('Lieutenant Charpentier', 195), ('Jane Porter', 168), ('Mr Philander', 100), ('Professor Porter', 95)]

__Alice's Adventures in Wonderland (Carroll)__

IS FIRST PERSON TEXT: False

Predicted gender of main character is 'Female' [('she', 492)]: True

CHARACTER OF INTEREST: [('Miss Alice', 369)]

ADDITIONAL TOP CHARACTERS OF INTEREST: [('Mock Turtle Soup', 62), ('Hatter', 55), ('Gryphon', 53), ('White Rabbit', 41), ('Dormouse', 40)]

__Jaberwocky (Carroll)__

IS FIRST PERSON TEXT: False

Predicted gender of main character is 'Male' [('He', 4)]: True

CHARACTER OF INTEREST: [('Jabberwock', 4)]

ADDITIONAL TOP CHARACTERS OF INTEREST: [('Callooh', 1), ('Jubjub', 1), ('Tumtum', 1), ('Bandersnatch', 1), ('Callay', 1)]

__The Mysterious Affair at Styles (Christie)__

IS FIRST PERSON TEXT: True

CHARACTER OF INTEREST: [('Monsieur Poirot', 374)]

ADDITIONAL TOP CHARACTERS OF INTEREST: [('Murder of Emily Agnes Inglethorp', 289), ('Monsieur John Cavendish', 201), ('Mr Hastings Miss Murdoch', 116), ('Mademoiselle Cynthia', 93), ('Mr Lawrence Cavendish', 76)]

__Heart of Darkness (Conrad)__

IS FIRST PERSON TEXT: True

CHARACTER OF INTEREST: [('Mistah Kurtz', 116)]

ADDITIONAL TOP CHARACTERS OF INTEREST: [('Company', 13), ('Charlie Marlow', 11), ('English', 10), ('Europe', 8), ('Russian', 7)]

__A Christmas Carol (Dickens)__

IS FIRST PERSON TEXT: False

CHARACTER OF INTEREST: [('Scrooge the Baleful', 329)]

ADDITIONAL TOP CHARACTERS OF INTEREST: [('Ghost of Christmas Present', 175), ('Evil Spirit', 79), ('Bob Cratchit', 51), ('Tiny Tim', 22), ('Master Peter Cratchit', 19)]

__A Tale of Two Cities (Dickens)__

IS FIRST PERSON TEXT: False

Predicted gender of main character is 'Male' [('his', 1940)]: True

CHARACTER OF INTEREST: [('Mr Jeremiah Cruncher', 180)]

ADDITIONAL TOP CHARACTERS OF INTEREST: [('Citizeness Defarge', 149), ('Madame Defarge', 120), ('Miss Pross', 110), ('Monsieur the Marquis', 102), ('Mr Carton', 96)]

__Great Expectations (Dickens)__

IS FIRST PERSON TEXT: True

CHARACTER OF INTEREST: [('Mrs Joe Gargery', 562)]

ADDITIONAL TOP CHARACTERS OF INTEREST: [('Memorandum of Herbert', 450), ('Miss Havisham', 309), ('Mr Pip', 268), ('Biddy', 230), ('Miss Estella', 228)]

__Sherlock Holmes (Doyle)__

IS FIRST PERSON TEXT: True

CHARACTER OF INTEREST: [('Mister Sherlock Holmes', 453)]

ADDITIONAL TOP CHARACTERS OF INTEREST: [('Dr Watson', 80), ('City of London', 51), ('Mr Lestrade of Scotland Yard', 48), ('Mr John Turner', 40), ('Mr James Windibank', 38)]

__The Hound of the Baskervillies (Doyle)__

IS FIRST PERSON TEXT: True

CHARACTER OF INTEREST: [('Sir William Baskerville', 299)]

ADDITIONAL TOP CHARACTERS OF INTEREST: [('Mr Sherlock Holmes', 192), ('Second Report of Dr Watson', 112), ('Dr James Mortimer', 93), ('Stapletons of Merripit House', 68), ('Mrs Barrymore', 66)]

__The Sign of Four (Doyle)__

IS FIRST PERSON TEXT: True

CHARACTER OF INTEREST: [('Mr Sherlock Holmes', 118)]

ADDITIONAL TOP CHARACTERS OF INTEREST: [('Mr Bartholomew Sholto', 72), ('Miss Mary Morstan', 37), ('Mr Athelney Jones', 33), ('Strange Story of Jonathan Small', 33), ('Toby', 26)]

__The Scarlet Letter (Hawthorne)__

IS FIRST PERSON TEXT: False

Predicted gender of main character is 'Female' [('her', 934)]: True

CHARACTER OF INTEREST: [('Madame Hester', 293)]

ADDITIONAL TOP CHARACTERS OF INTEREST: [('Little Pearl', 202), ('Mr Dimmesdale', 71), ('Old Roger Chillingworth', 56), ('Reverend Master Dimmesdale', 54), ('New England Clergyman', 39)]

__Metamorphosis (Kafka)__

IS FIRST PERSON TEXT: False

Predicted gender of main character is 'Male' [('his', 524)]: True

CHARACTER OF INTEREST: [('Gregor Samsa', 296)]

ADDITIONAL TOP CHARACTERS OF INTEREST: [('Grete', 25), ('Mr Samsa', 21), ('Mrs Samsa', 10), ('God', 7), ('Christmas', 3)]

__The Trial (Kafka)__

IS FIRST PERSON TEXT: False

Predicted gender of main character is 'Male' [('he', 1699)]: False

CHARACTER OF INTEREST: [('Miss Montag', 101)]

ADDITIONAL TOP CHARACTERS OF INTEREST: [('Leni', 94), ('Mrs Grubach', 77), ('Fetch Block', 55), ('Mr Block', 54), ('Italian', 34)]

__The Jungle Book (Kipling)__

IS FIRST PERSON TEXT: False

Predicted gender of main character is 'Male' [('he', 865)]: True

CHARACTER OF INTEREST: [('Song of Mowgli', 170)]

ADDITIONAL TOP CHARACTERS OF INTEREST: [('Bagheera of the Council Rock', 161), ('Baloo of the Seeonee Wolf Pack', 125), ('Kala Nag', 98), ('Valiant Rikki-tikki', 95), ('Little Nightingale Island', 91)]

__The Call of the Wild (London)__

IS FIRST PERSON TEXT: False

Predicted gender of main character is 'Male' [('he', 616)]: True

CHARACTER OF INTEREST: [('Buck', 358)]

ADDITIONAL TOP CHARACTERS OF INTEREST: [('John Thornton', 102), ('Spitz', 60), ('Francois', 60), ('Perrault', 39), ('Hal', 37)]

__White Fang (London)__

IS FIRST PERSON TEXT: False

Predicted gender of main character is 'Male' [('he', 1531)]: True

CHARACTER OF INTEREST: [('White Fang', 569)]

ADDITIONAL TOP CHARACTERS OF INTEREST: [('Grey Beaver', 119), ('Henry', 95), ('Beauty Smith', 84), ('Matt', 82), ('Bill', 81)]

__Love in the Time of Cholera (Marquez)__

IS FIRST PERSON TEXT: False

Predicted gender of main character is 'Male' [('he', 2921)]: True

CHARACTER OF INTEREST: [('Dr Marco Aurelio Urbino Daza', 820)]

ADDITIONAL TOP CHARACTERS OF INTEREST: [('Pentecost Communion', 47), ('Cousin Hildebranda Sanchez', 33), ('Jeremiah de Saint-Amour', 32), ('Plaza of the Customhouse', 28), ('secret', 22)]

__1984 (Orwell)__

IS FIRST PERSON TEXT: False

CHARACTER OF INTEREST: [('Winston Smith', 486)]

ADDITIONAL TOP CHARACTERS OF INTEREST: [('Labour Party', 231), ("O'Brien", 190), ("'the Party", 121), ('Eleventh Edition of the Newspeak Dictionary', 104), ('Big Brother', 63)]
 
__Raven (Poe)__

IS FIRST PERSON TEXT: True

CHARACTER OF INTEREST: [('Quoth the Raven', 10)]

ADDITIONAL TOP CHARACTERS OF INTEREST: [('Lenore', 8), ('Nevermore', 8), ('Perched', 2), ('December', 2), ('Night', 2)]

__Frankenstein (Shelley)__

IS FIRST PERSON TEXT: True

CHARACTER OF INTEREST: [('Elizabeth Lavenza', 80)]

ADDITIONAL TOP CHARACTERS OF INTEREST: [('Henry Clerval', 72), ('Justine Moritz', 52), ('Felix', 49), ('Genevan', 35), ('Victor', 23)]

__The Strange Case of Dr. Jekyll and Mr. Hyde (Stevenson)__

IS FIRST PERSON TEXT: True

CHARACTER OF INTEREST: [('Mr Utterson of Gaunt Street', 126)]

ADDITIONAL TOP CHARACTERS OF INTEREST: [('Dr Henry Jekyll', 62), ('Edward Hyde', 60), ('Poole', 58), ('Dr Lanyon', 30), ('Mr Hyde', 27)]

__Treasure Island (Stevenson)__

IS FIRST PERSON TEXT: True

CHARACTER OF INTEREST: [('Long John Silver', 295)]

ADDITIONAL TOP CHARACTERS OF INTEREST: [('Jim Hawkins', 96), ('Doctor Livesey', 63), ('Admiral Benbow', 52), ('Captain Flint', 50), ('Tom Redruth', 46)]

__Dracula (Stoker)__

IS FIRST PERSON TEXT: True

CHARACTER OF INTEREST: [('Dr Van Helsing', 306)]

ADDITIONAL TOP CHARACTERS OF INTEREST: [('Professor Van Helsing', 284), ('Abraham Van Helsing', 281), ('Honourable Arthur Holmwood', 168), ('Fenchurch Street Lord Godalming', 168), ('Dr John Seward', 113)]

__Adventures of Tom Sawyer (Twain)__

IS FIRST PERSON TEXT: False

CHARACTER OF INTEREST: [('Tom Sawyer the Pirate', 795)]

ADDITIONAL TOP CHARACTERS OF INTEREST: [('Huck Finn the Red-Handed', 244), ('Joe Harper', 147), ('Mr Siddy', 66), ('Daily Muff Potter', 46), ('Aunt Polly', 45)]

__20,000 Leagues Under the Sea (Verne)__

IS FIRST PERSON TEXT: True

CHARACTER OF INTEREST: ('Captain Nemo', 283)

TOP CHARACTERS OF INTEREST: [('Commander of the Nautilus', 195), ('Conseil', 193), ('Canadian', 144), ('Captain Denham of the Herald', 126)]

__Around the World in Eighty Days (Verne)__

IS FIRST PERSON TEXT: False

Predicted gender of main character is 'Male' [('his', 807)]: True

CHARACTER OF INTEREST: [('Monsieur Phileas Fogg', 600)]

ADDITIONAL TOP CHARACTERS OF INTEREST: [('Jean Passepartout', 365), ('Mr Passepartout', 363), ('Monsieur Fix', 243), ('Aouda', 128), ('Illustrated London News', 63)]

__The Island of Doctor Moreau (Wells)__

IS FIRST PERSON TEXT: True

CHARACTER OF INTEREST: [('Montgomery', 202)]

ADDITIONAL TOP CHARACTERS OF INTEREST: [('Island of Doctor Moreau', 136), ('Beast People', 74), ('Sayer of the Law', 61), ("M'ling", 40)]

__The War of the Worlds (Wells)__

IS FIRST PERSON TEXT: True

CHARACTER OF INTEREST: [('Repulse of the Martians', 83)]

ADDITIONAL TOP CHARACTERS OF INTEREST: [('Pool of London', 48), ('Old Woking', 45), ('Heat-Ray', 27), ('Mars', 24), ('Ogilvy', 22)]

__Time Machine (Wells)__

IS FIRST PERSON TEXT: True

CHARACTER OF INTEREST: [('Time Traveller', 104)]

ADDITIONAL TOP CHARACTERS OF INTEREST: [("'Little Weena", 49), ('Advancement of Mankind', 28), ('Psychologist', 22), ('moon', 19), ('Editor', 19)]

__My Man Jeeves (Wodehouse)__

IS FIRST PERSON TEXT: True

CHARACTER OF INTEREST: [('Jeeves', 233)]

ADDITIONAL TOP CHARACTERS OF INTEREST: [('Mr Blooming Lattaker', 101), ('Rocky Todd', 60), ('Old Bicky', 57), ('Bobbie Cardew', 56), ('Corky', 53)]

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
