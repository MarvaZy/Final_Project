# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 22:24:17 2020

@author: MarvaZychlinski
"""
from BaseCrawler import BaseCrawler

# first we need to import our database in mySQL
from db import db

class Search(db):
    
    def __init__(self):
        super(Search, self).__init__()
    
    def _type_error(self, list_of_words):
        '''
        checks for typing errors of user's input
        output - list of words 
        user chooses whether to change his input or not
        '''
        errors = list_of_words.copy()
        correct_words = list_of_words.copy()
        for i in BaseCrawler.category_dictionary.keys():
            records = self.select(BaseCrawler.category_dictionary[i]["English"])
            # casting to a list only the ingredients
            if len(records) > 0:
                ingr = [i.split() for i in (list(list(zip(*records))))[2]]
                ingr_flat = [item for sublist in ingr for item in sublist]
                for word in errors: 
                    if word in ingr_flat:
                        errors.remove(word)
                    if len(errors) == 0:
                        break
            else:
                pass
        # if errors list still have values, it means no match was found for them
        if len(errors):
            print("ייתכן והייתה שגיאה בקלט שהוזן. המילים הבאות לא נמצאו במאגרינו: ", end="")
            print(*errors)
            another_input = input("לשיקולך, הזן כעת את בחירותייך בשנית. אם אינך מעוניין לשנות את בחירותייך, הקש אנטר\n").split()
            if len(another_input):
                correct_words = another_input
                
        return correct_words
    
    def _index_to_category(self, index):
        """
        index_to_category translate the number that the user will choose as its category, to the related table
        """
        if index in BaseCrawler.category_dictionary.keys():
            category = BaseCrawler.category_dictionary[index]["English"]
        # this will not happen - this function is acctivated only if the input is between 1 to 8
        else:
            return "Error"
        
        return category

    def _singular_to_ploral(self, list_of_words):
        '''
        singular_to_ploral: for words in final form in Hebrew in a given list, this function deletes their last char for more results in search
        '''
        words = list_of_words.copy()
        special_char = ["ן", "נ", "פ", "ף", "ם", "מ", "כ", "ך", "צ", "ץ"]
        for word in words:
            if word[-1] in special_char and word != "גלוטן":
                words.remove(word)
                words.append(word[:-1])
        
        return words
    
    def search(self):
        '''
        the search algorithm - first the user will choose the kind of recipe he's looking for
        than he will input the restrictions and preferences
        '''
        recipes = {}
        usr_input = input("מהו סוג המתכון המבוקש? (הקש את המספר)\n1. ארוחות בוקר\n2. עיקריות \n3. קינוחים ומתוקים\n4. סלטים\n5. נשנושים וחטיפים\n6. שייקים ומשקאות\n7. גבינות וממרחים\n")
        try:
            while int(usr_input) not in range(1,8):
                usr_input = int(input("בחירה לא חוקית; אנא בחר שנית:\n1. ארוחות בוקר\n2. עיקריות\n3. קינוחים ומתוקים\n4. סלטים\n5. נשנושים וחטיפים\n6. שייקים ומשקאות\n7. גבינות וממרחים\n"))
        except ValueError:
            usr_input = print("בחירה לא חוקית; אנא בחר שנית")
            self.search()
        records = self.select(self._index_to_category(int(usr_input)))
        # checks for possible type errors in user input
        restrictions = self._singular_to_ploral(self._type_error(input("מהן המגבלות התזונתיות? (ניתן לבחור יותר מאחד, יש להקיש רווח בין בחירה לבחירה. אנא כתבו רכיבים בצורת יחיד)\n").split()))
        preferences = self._singular_to_ploral(self._type_error(input("אילו מצרכים תרצה שיכללו במתכון? (ניתן לבחור יותר מאחד, יש להקיש רווח בין בחירה לבחירה. אנא כתבו רכיבים בצורת יחיד)\n").split()))
        # all of the urls in the choosen category - for gluten option check
        urls = []
        # choosing recipe by input
        for name, url, ingr in records:
            urls.append(url)
            if all(x in ingr for x in preferences) and all(x not in ingr for x in restrictions):
                recipes[name] = url

        # if gluten is entered as restriction, algorithm will add the relevant recipes from the gluten cloumn in our table
        if 'גלוטן' in restrictions:
            # no gluten recipes
            no_gluten = self.select("Gluten") 
            restrictions.remove('גלוטן')
            for name, url, ingr in no_gluten:
                if url in urls:
                    if all(x in ingr for x in preferences) and all(x not in ingr for x in restrictions):
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
            another_search = input("לא נמצאו מתכונים מתאימים. להרצת חיפוש חדש, הקש 1 ולחץ אנטר\n")
            if another_search == "1":
                return self.search()

search = Search()
search.search()
