# -*- coding: utf-8 -*-
"""
Created on Sun Sep 20 12:34:47 2020

@author: MarvaZychlinski
"""

'''
Creating the database for the project
'''

# first we need to import our server in mySQL
import mysql.connector as mysql

db = mysql.connect(
    host = "localhost",
    user = "root",
    passwd = "123456789"
)

cursor = db.cursor()


# This line created the database
cursor.execute("CREATE DATABASE final_project")     

# Now we can acssess the database
mydb = mysql.connect(
    host = "localhost",
    user = "root",
    passwd = "123456789",
    database = "final_project"
)

mycursor = mydb.cursor()

'''
Creating all the tables in our database
Gluten table contains gluten-free recipes
'''
mycursor.execute("CREATE TABLE Breakfast (id INT AUTO_INCREMENT PRIMARY KEY, Name VARCHAR(255), URL VARCHAR(255), Ingredients VARCHAR(10000))")
mycursor.execute("CREATE TABLE MainCourse (id INT AUTO_INCREMENT PRIMARY KEY, Name VARCHAR(255), URL VARCHAR(255), Ingredients VARCHAR(10000))")
mycursor.execute("CREATE TABLE Dessert (id INT AUTO_INCREMENT PRIMARY KEY, Name VARCHAR(255), URL VARCHAR(255), Ingredients VARCHAR(10000))")
mycursor.execute("CREATE TABLE Salad (id INT AUTO_INCREMENT PRIMARY KEY, Name VARCHAR(255), URL VARCHAR(255), Ingredients VARCHAR(10000))")
mycursor.execute("CREATE TABLE Snack (id INT AUTO_INCREMENT PRIMARY KEY, Name VARCHAR(255), URL VARCHAR(255), Ingredients VARCHAR(10000))")
mycursor.execute("CREATE TABLE Shake (id INT AUTO_INCREMENT PRIMARY KEY, Name VARCHAR(255), URL VARCHAR(255), Ingredients VARCHAR(10000))")
mycursor.execute("CREATE TABLE Spread (id INT AUTO_INCREMENT PRIMARY KEY, Name VARCHAR(255), URL VARCHAR(255), Ingredients VARCHAR(10000))")
mycursor.execute("CREATE TABLE Gluten (id INT AUTO_INCREMENT PRIMARY KEY, Name VARCHAR(255), URL VARCHAR(255), Ingredients VARCHAR(10000))")