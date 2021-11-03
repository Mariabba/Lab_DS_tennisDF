# Lab_DS_tennisDF

##  Introduction
In Part 1 of the project you are required to create and populate a database starting from .csv
les and perform dierent operations on it. In the following you can nd a set of incremental
assignments, each one with a brief description of what you are required to produce and what
tools you can use for the task.

##  Build the datawarehouse
tennis.csv contains the main body of data: a fact table with tennis match data. For each
match we have information about the tournament, the players involved (winner and loser)
and several other metrics.
Files male players.csv and female players.csv contain the list of male players and
female players respectively, while geography.csv contain a list of IOC codes with country
names and continents.
In these four les you will nd all the attributes to reproduce the schema shown in 1.
The le tennis.csv will have to be split appropriately and combined with the other les to
achieve this goal.
The goal of the following assignments is to build the schema and deploy it on server
lds.di.unipi.it. Beware that, just as in real-life scenario, les may contain missing values
and/or slight mistakes.

### Assignment 0
Create the database schema in Figure 1 using SQL Server Management Studio in
server lds.di.unipi.it. The name of the database must be GroupIDHWMart (exam-
ple: Group01HWMart).

### Assignment 1
Write a python program that splits the content of tennis.csv into four separate
tables: match, tournament, date and player. Use the les male players.csv and
female plauyers.csv to create the attribute "sex" for the player table. The use
of the pandas library is forbidden for this assingment.

### Assignment 2
Write a Python program that populates the database GroupIDHWMart with the
various tables from the .csv les, establishing schema relations as necessary.


![](../../OneDrive/Desktop/Immagine.png)