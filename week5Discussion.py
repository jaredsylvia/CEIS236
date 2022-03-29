# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 12:42:32 2022

@author: jared
"""

import mysql.connector

ceis236db = mysql.connector.connect(
  host="10.10.0.2",
  user="ceis236",
  password="ceis236",
  database="CEIS236"
)



cursor = ceis236db.cursor()

cursor.execute("""CREATE TABLE player (
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
    """)

cursor.execute("""CREATE TABLE item (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(12) NOT NULL,
    description MEDIUMTEXT NOT NULL,
    PRIMARY KEY(id)
    );
    """)
    
cursor.execute("""CREATE TABLE inventory (
    slot INT NOT NULL,
    itemID INT NOT NULL,
    playerID INT NOT NULL,
    PRIMARY KEY(playerID,slot),
    FOREIGN KEY(playerID) REFERENCES player(id),
    FOREIGN KEY(itemID) REFERENCES item(id)
    );
    """)