# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 09:32:09 2020

@author: MarvaZychlinski
"""
import mysql.connector as mysql

class db:
    def __init__(self):
        '''acssess the database'''
        self.mydb = mysql.connect(
            host = "localhost",
            user = "root",
            passwd = "123456789",
            database = "final_project"
        )
        self.mycursor = self.mydb.cursor()
        self.category_dictionary = {1: {"English": "Breakfast", "Hebrew": "ארוחות בוקר"}, 
                                    2: {"English": "MainCourse", "Hebrew": "עיקריות"}, 
                                    3: {"English": "Dessert", "Hebrew": "קינוחים ומתוקים"},
                                    4: {"English": "Salad", "Hebrew": "סלטים"},
                                    5: {"English": "Snack", "Hebrew": "נשנושים וחטיפים"},
                                    6: {"English": "Shake", "Hebrew": "שייקים ומשקאות"},
                                    7: {"English": "Spread", "Hebrew": "גבינות וממרחים"},
                                    8: {"English": "Gluten", "Hebrew": "נטול גלוטן"}                    
                                    }

    def _get_ingredients(self, category):
        pass
    
    def insert(self):
        '''
        insert all the data of the recipes from a website to the SQL table
        ''' 
        sql_statement = ["INSERT INTO ","category"," (Name, URL, Ingredients) VALUES (%s, %s, %s)"]
        for index in self.category_dictionary:
            try:
                sql_statement[1] = self.category_dictionary[index]["English"]
                sql = ''.join(sql_statement)
                ingerdients_dic = self._get_ingredients(self.category_dictionary[index]["Hebrew"])
                for recipe in ingerdients_dic:
                    url_adr = ingerdients_dic[recipe]["url"]
                    ingr_list = ingerdients_dic[recipe]["ingredients"]
                    val = (str(recipe), str(url_adr), str(ingr_list))
                    self.mycursor.execute(sql, val)
                    self.mydb.commit()
            except:
                pass
        return
    
    def select(self, index):        
        """
        select translate the number that the user will choose as its category, to the related table
        """
        sql_select_list = ["SELECT Name, URL, Ingredients FROM ", "category"]
        if index in range(1,9):
            sql_select_list[1] = self.category_dictionary[index]["English"]
            sql_select_query = ''.join(sql_select_list)
            self.mycursor.execute(sql_select_query)
            records = self.mycursor.fetchall()       
        # this will not happen - this function is acctivated only if the input is between 1 to 8
        else:
            records = "Error"
         
        return records
