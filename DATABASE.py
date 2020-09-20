# -*- coding: utf-8 -*-
"""
Created on Sun Sep 20 12:34:47 2020

@author: MarvaZychlinski
"""

'''
Creating the database for the project
'''

import mysql.connector as mysql

db = mysql.connect(
    host = "localhost",
    user = "root",
    passwd = "123456789"
)

cursor = db.cursor()

# cursor.execute("CREATE DATABASE final_project")     This line created the database

mydb = mysql.connect(
    host = "localhost",
    user = "root",
    passwd = "123456789",
    database = "final_project"
)

mycursor = mydb.cursor()

mycursor.execute("CREATE TABLE Ingredients_Table (id INT AUTO_INCREMENT PRIMARY KEY, Category VARCHAR(255), URL VARCHAR(255), Ingredients VARCHAR(10000))")    #This line created a table - first column is id number, than category, than url and the last column is the ingredients

