# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 09:32:09 2020

@author: MarvaZychlinski
"""
import mysql.connector as mysql

class db():
    
    def __init__(self):
        '''access the database'''
        self.mydb = mysql.connect(
            host = "localhost",
            user = "root",
            passwd = "123456789",
            database = "final_project"
        )
        self.mycursor = self.mydb.cursor()
    
    def insert(self, eng_category, recipe_name, url, ingredients):
        '''
        insert one row of data to the SQL table
        ''' 
        sql = "INSERT INTO " + str(eng_category) + " (Name, URL, Ingredients) VALUES (%s, %s, %s)"
        val = (str(recipe_name), str(url), str(ingredients))
        self.mycursor.execute(sql, val)
        self.mydb.commit()

        return
    
    def select(self, eng_category):        
        """
        select translate the number that the user will choose as its category, to the related table
        """
        sql_select_query = "SELECT Name, URL, Ingredients FROM "+ str(eng_category)
        self.mycursor.execute(sql_select_query)
        records = self.mycursor.fetchall()
         
        return records
    
    def bulk_insert(self, eng_category, ingr_dictionary):
        '''
        insert multiple rows of data to the SQL table
        '''
        try:
            for recipe_name in ingr_dictionary:
                url = ingr_dictionary[recipe_name]["url"]
                ingredients = ingr_dictionary[recipe_name]["ingredients"]
                self.insert(eng_category, recipe_name, url, ingredients)
        except:
            pass
        
