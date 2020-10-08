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

import MarkivSodi
import Tivoneat
import TheVeganati
import Veg

def enter_categories(website):
    '''
    enter_categories - 
    value "website" - the name of the class representing each website
    '''
    category_dictionary = {
"ארוחות בוקר": "Breakfast",                       
"עיקריות": "MainCourse",                       
"קינוחים ומתוקים": "Dessert",                       
"סלטים": "Salad",                       
"נשנושים וחטיפים": "Snack",                       
"שייקים ומשקאות": "Shake",                       
"גבינות וממרחים": "Spread",                       
"נטול גלוטן": "Gluten",                       
                     }
    sql_statement = ["INSERT INTO ","category"," (Name, URL, Ingredients) VALUES (%s, %s, %s)"]
    for category in category_dictionary:
        try:
            sql_statement[1] = category_dictionary[category]
            sql = ''.join(sql_statement)
            ingerdients_dic = website.get_ingredients(category)
            for recipe in ingerdients_dic:
                url_adr = ingerdients_dic[recipe]["url"]
                ingr_list = ingerdients_dic[recipe]["ingredients"]
                val = (str(recipe), str(url_adr), str(ingr_list))
                mycursor.execute(sql, val)
                mydb.commit()
        except:
            pass
    return 

# this code entered all the information from TIVONEAT, Markiv Sodi and TheVeganati websites to our database
Tivoneat = Tivoneat.Tivoneat()
MarkivSodi = MarkivSodi.MarkivSodi()
TheVeganati = TheVeganati.TheVeganati()
Veg = Veg.Veg()
enter_categories(Tivoneat)   
enter_categories(MarkivSodi) 
enter_categories(TheVeganati)
enter_categories(Veg)    