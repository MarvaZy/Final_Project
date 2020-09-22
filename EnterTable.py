# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 21:32:42 2020

@author: MarvaZychlinski
"""

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
    categories = list(dict.fromkeys(categories))
    num_categories = len(categories)
    for i in range(num_categories):
        category_name = categories[i][0]
        ingedients_matrix = website._get_ingredients(i)
        for j in range(len(ingedients_matrix)):
            url_adr = ingedients_matrix[j][0]
            ingr_list = ingedients_matrix[j][1]
            
            sql = "INSERT INTO Ingredients_Table (Category, URL, Ingredients) VALUES (%s, %s, %s)"
            val = (str(category_name), str(url_adr), str(ingr_list))
            cursor.execute(sql, val)

            db.commit()
    return
               

enter_table(Tivoneat)   #--> this code entered all the information from TIVONEAT website to our database
    