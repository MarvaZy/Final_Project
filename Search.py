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
        restrictions = input("מהן המגבלות התזונתיות? (ניתן לבחור יותר מאחד, יש להקיש רווח בין בחירה לבחירה)\n").split()
        preferences = input("אילו מצרכים תרצה שיכללו במתכון? (ניתן לבחור יותר מאחד, יש להקיש רווח בין בחירה לבחירה)\n").split()
        # all of the urls in the choosen category - for gluten option check
        urls = []
        # choosing recipe by input
        for name, url, ingr in records:
            urls.append(url)
            if not any(x in ingr for x in restrictions) and all(x in ingr for x in preferences):
                recipes[name] = url

        # if gluten is entered as restriction, algorithm will add the relevant recipes from the gluten cloumn in our table
        if 'גלוטן' in restrictions:
            # no gluten recipes -> index = 8
            no_gluten = self.select(8) 
            restrictions.remove('גלוטן')
            for name, url, ingr in no_gluten:
                if url in urls:
                    if not any(x in ingr for x in restrictions) and all(x in ingr for x in preferences):
                        recipes[name] = url
       # if no results were found, user will be able to start a new search
        if recipes:
            # prints with empty line, separating the user input to the output, and from one recipe to the other
            print("")
            for recipe in recipes:
                print(recipe)
                print(recipes[recipe])
                print("")
        else:
            # checks for typing errors of user's input
            pref_and_rest = preferences + restrictions
            i=1
            while i<=1:
                records = self.select(i)
                ingr = [i.split() for i in list(list(zip(*records)))[2]]
                ingr_flat = [item for sublist in ingr for item in sublist]
                for word in pref_and_rest: 
                    if word in ingr_flat:
                        print(word)
                        pref_and_rest.remove(word)
                    if len(pref_and_rest) == 0:
                        break
                i += 1
            # if a word is not found anywhere in the ingredients database, it may be a typing error
            if len(pref_and_rest):
                print("ייתכן והייתה שגיאה בקלט שהוזן. המילים הבאות לא נמצאו במאגרינו: ", end="")
                print(*pref_and_rest)
                another_search = input("להרצת חיפוש חדש, הקש 1 ולחץ אנטר\n")
            else:
                another_search = input("לא נמצאו מתכונים מתאימים. להרצת חיפוש חדש, הקש 1 ולחץ אנטר\n")
            if another_search == "1":
                return self.search()   

search = Search()
search.search()
