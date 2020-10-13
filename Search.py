# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 22:24:17 2020

@author: MarvaZychlinski
"""

# first we need to import our database in mySQL
from db import db

class Search(db):
    
    def __init__(self):
        super(Search, self).__init__()
 
    def search(self):
        '''
        the search algorithm - first the user will choose the kind of recipe he's looking for
        than he will input the restrictions and preferences
        '''
        recipes = {}
        usr_input = int(input("מהו סוג המתכון המבוקש? (הקש את המספר)\n1. ארוחות בוקר\n2. עיקריות \n3. קינוחים ומתוקים\n4. סלטים\n5. נשנושים וחטיפים\n6. שייקים ומשקאות\n7. גבינות וממרחים\n"))
        while usr_input not in range(1,8):
            usr_input = int(input("בחירה לא חוקית; אנא בחר שנית:\n1. ארוחות בוקר\n2. עיקריות\n3. קינוחים ומתוקים\n4. סלטים\n5. נשנושים וחטיפים\n6. שייקים ומשקאות\n7. גבינות וממרחים\n"))
        records = self.select(usr_input)
        restrictions = input("מהן המגבלות התזונתיות? (ניתן לבחור יותר מאחד, יש להקיש רווח בין בחירה לבחירה)\n")
        restrictions_list = restrictions.split()
        preferences = input("אילו מצרכים תרצה שיכללו במתכון? (ניתן לבחור יותר מאחד, יש להקיש רווח בין בחירה לבחירה)\n")
        preferences_list = preferences.split()
        # all of the urls in the choosen category - for gluten option check
        urls = []
        # choosing recipe by input
        for name, url, ingr in records:
            urls.append(url)
            if not any(x in ingr for x in restrictions_list) and all(x in ingr for x in preferences_list):
                recipes[name] = url

        # if gluten is entered as restriction, algorithm will add the relevant recipes from the gluten cloumn in our table
        if 'גלוטן' in restrictions_list:
            # no gluten recipes -> index = 8
            no_gluten = self.select(8) 
            restrictions_list.remove('גלוטן')
            for name, url, ingr in no_gluten:
                if url in urls:
                    if not any(x in ingr for x in restrictions_list) and all(x in ingr for x in preferences_list):
                        recipes[name] = url
        
        return recipes   

search = Search()
print(search.search())
