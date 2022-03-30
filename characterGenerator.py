# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 12:42:32 2022

@author: jared
"""

import mysql.connector
import random

ceis236db = mysql.connector.connect(    # Set up SQL connection information
  host="10.10.0.2",
  user="ceis236",
  password="ceis236",
  database="CEIS236"
)
cursor = ceis236db.cursor() # Define cursor

tableCreationCmds = ["""CREATE TABLE IF NOT EXISTS player (  
    id INT NOT NULL AUTO_INCREMENT,
    strength INT NOT NULL,
    dexterity INT NOT NULL,
    constituion INT NOT NULL,
    intelligence INT NOT NULL,
    wisdom INT NOT NULL,
    charisma INT NOT NULL,
    name VARCHAR(12) NOT NULL,
    class VARCHAR(12) NOT NULL,
    level INT NOT NULL,
    PRIMARY KEY(id)
    );
    """,
    """CREATE TABLE IF NOT EXISTS item (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(12) NOT NULL,
    description MEDIUMTEXT NOT NULL,
    PRIMARY KEY(id)
    );
    """,
    """CREATE TABLE IF NOT EXISTS inventory (
    slot INT NOT NULL,
    itemID INT NOT NULL,
    playerID INT NOT NULL,
    PRIMARY KEY(playerID,slot),
    FOREIGN KEY(playerID) REFERENCES player(id),
    FOREIGN KEY(itemID) REFERENCES item(id)
    );
    """] ### SQL queries for table creation

for i in tableCreationCmds:
    cursor.execute(i)  ## Loop through and run each defined query

charOrItem = False ## Set initial value to run while loop

def createCharacter():
    name = str(input("Character Name: "))
    charClass = str(input("Character Class: "))
    startingLevel = int(input("Starting Level: "))
    strength = random.randint(3,18) + (startingLevel - 1)
    dexterity =  random.randint(3,18) + (startingLevel - 1)
    constitution = random.randint(3,18) + (startingLevel - 1)
    intelligence = random.randint(3,18) + (startingLevel - 1)
    wisdom = random.randint(3,18) + (startingLevel - 1)
    charisma = random.randint(3,18) + (startingLevel - 1)
    fullChar = {"name" : name, "charClass": charClass, "level" : startingLevel,
        "attributes" : {
        "strength": strength,
        "dexterity": dexterity,
        "constituion": constitution,
        "intelligence": intelligence,
        "wisdom": wisdom,
        "charisma": charisma}}
    return(fullChar)

def createItem():
    name = str(input("Item Name: "))
    description = str(input("Item Description: "))
    return({"item": name, "itemdesc": description})

def insertToSQL(table, objDict):
    if(table == 'player'):
        print("Inserting player into database...")
        print(objDict)
        cursor.execute("""INSERT INTO player(
            name, class, level, strength, dexterity, constituion,
            intelligence, wisdom, charisma)
        VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (objDict['name'], objDict['charClass'], 
        objDict['level'],
        objDict['attributes']['strength'], 
        objDict['attributes']['dexterity'], 
        objDict['attributes']['constituion'], 
        objDict['attributes']['intelligence'], 
        objDict['attributes']['wisdom'],
        objDict['attributes']['charisma']))
        cursor.execute('COMMIT;')
    elif(table == 'item'):
        print(objDict)
        cursor.execute("""INSERT INTO item (
            name, description)
        VALUES (
            %s, %s)""", (objDict['item'], objDict['itemdesc']))
        cursor.execute('COMMIT;')
        print("Inserting item into database...")
    else:
        print("Did not receive valid directives.")


while (charOrItem != 'q'):
    try:
        charOrItem = str(input("Press (Q) to quit.\nCreate new (C)haracter or new (I)tem? ")).lower()
        print(charOrItem)
        if(charOrItem == 'c'):
            insertToSQL('player', createCharacter())
        elif(charOrItem == 'i'):
            insertToSQL('item', createItem())
        elif(charOrItem == 'q'):
            print("Quitting")
            
            
    except:
        print("An exception has occured")
