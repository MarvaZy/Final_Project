# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 21:32:42 2020

@author: MarvaZychlinski
"""
import MarkivSodi
import Tivoneat
import mysql.connector as mysql

db = mysql.connect(
    host = "localhost",
    user = "root",
    passwd = "123456789",
    database = "final_project"
)

cursor = db.cursor()


def enter_table(website):
    
    '''
    enter_table - enters all the information gathered from TIVONEAT website into the table
    value "website" - the name of the class representing each website
    '''
    
    categories = website._get_categories()
    num_categories = len(categories)
    for i in range(num_categories):
        category_name = categories[i][0]
        ingredients_matrix = website._get_ingredients(i)
        for j in range(len(ingredients_matrix)):
            rec_name = ingredients_matrix[j][0]
            url_adr = ingredients_matrix[j][1]
            ingr_list = ingredients_matrix[j][2]
            
            sql = "INSERT INTO Ingredients_Table (Category, Name, URL, Ingredients) VALUES (%s, %s, %s, %s)"
            val = (str(category_name), str(rec_name), str(url_adr), str(ingr_list))
            cursor.execute(sql, val)

            db.commit()
    
    return
               

# this code entered all the information from TIVONEAT and Markiv Sodi website to our database
enter_table(Tivoneat)   
enter_table(MarkivSodi)   