# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 22:24:17 2020

@author: MarvaZychlinski
"""

# first we need to import our database in mySQL

import mysql.connector as mysql

db = mysql.connect(
    host = "localhost",
    user = "root",
    passwd = "123456789",
    database = "final_project"
)

cursor = db.cursor()

class Search:
    
    def __init__(self):
        pass

    def _category_from_index(self, index):
        
        """
        category_from_index translate the number that the user will choose as its category, to the related categories in our table
        """
        
        if index == 1:
            sql_select_query = """SELECT URL, Ingredients FROM Ingredients_Table WHERE Category LIKE '%בוקר%'"""
            cursor.execute(sql_select_query)
            records = cursor.fetchall()
            
        elif index == 2:
            sql_select_query = """SELECT URL, Ingredients FROM Ingredients_Table WHERE Category LIKE '%עיקריות%'"""
            cursor.execute(sql_select_query)
            records = cursor.fetchall()
            
        elif index == 3:
            sql_select_query = """SELECT URL, Ingredients FROM Ingredients_Table WHERE Category LIKE '%קינוחים%'"""
            cursor.execute(sql_select_query)
            records = cursor.fetchall()
            
        elif index == 4: 
            sql_select_query = """SELECT URL, Ingredients FROM Ingredients_Table WHERE Category LIKE '%סלטים%'"""
            cursor.execute(sql_select_query)
            records = cursor.fetchall()
            
        elif index == 5: 
            sql_select_query = """SELECT URL, Ingredients FROM Ingredients_Table WHERE Category LIKE '%נשנושים%'"""
            cursor.execute(sql_select_query)
            records = cursor.fetchall()
            
        elif index == 6:
            sql_select_query = """SELECT URL, Ingredients FROM Ingredients_Table WHERE Category LIKE '%שייקים%'"""
            cursor.execute(sql_select_query)
            records = cursor.fetchall()
            
        elif index == 7:
            sql_select_query = """SELECT URL, Ingredients FROM Ingredients_Table WHERE Category LIKE '%גבינות%'"""
            cursor.execute(sql_select_query)
            records = cursor.fetchall()
            
        # this will not happen - this function is acctivated only if the input is between 1 to 7
        else:
            records = "Error"
         
        return records
    
    def _gluten(self):
        
        '''
        gluten function gives all the records related to no-gluten recipies 
        '''
        
        sql_select_query = """SELECT URL, Ingredients FROM Ingredients_Table WHERE Category LIKE '%גלוטן%'"""
        cursor.execute(sql_select_query)
        no_gluten = cursor.fetchall()
    
        return no_gluten
   
    def search(self):
        
        '''
        the search algorithm - first the user will choose the kind of recipe he's looking for
        than he will input the restrictions
        '''
        
        no_gluten = Search._gluten()
        
        url_list = []
        usr_input = int(input("מהו סוג המתכון המבוקש? (הקש את המספר)\n1. ארוחות בוקר\n2. עיקריות \n3. קינוחים ומתוקים\n4. סלטים\n5. נשנושים וחטיפים\n6. שייקים ומשקאות\n7. גבינות וממרחים\n"))
        while usr_input not in range(1,8):
            usr_input = int(input("בחירה לא חוקית; אנא בחר שנית:\n1. ארוחות בוקר\n2. עיקריות\n3. קינוחים ומתוקים\n4. סלטים\n5. נשנושים וחטיפים\n6. שייקים ומשקאות\n7. גבינות וממרחים\n"))
        records = Search._category_from_index(usr_input)
        
        
        restrictions = input("מהן המגבלות התזונתיות? (ניתן לבחור יותר מאחד, יש להקיש רווח בין בחירה לבחירה)\n")
        restrictions_list = restrictions.split()
        
        for url, ingr in records:
            if not all(x in ingr for x in restrictions_list):
                url_list.append(url)
        
        urls = []
        for url, ingr in records:
            urls.append(url)
        
        # if gluten is entered as restriction, algorithm will add the relevant recipes from the gluten cloumn in our table
        if 'גלוטן' in restrictions_list:    
            restrictions_list.remove('גלוטן')
            for url, ingr in no_gluten:
                if url in urls:
                    if not all(x in ingr for x in restrictions_list):
                        url_list.append(url) 
        return url_list   


print(Search.search())

