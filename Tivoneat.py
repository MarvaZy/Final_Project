# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 20:22:12 2020

@author: MarvaZychlinski
"""

'''
For Tivoneat Website Only
'''


import requests
from bs4 import BeautifulSoup



class Tivoneat:
    
    def __init__(self):
        self.url = "https://tivoneat.co.il/"                                   # home page of one of the recipes' websites

    
    def _get_categories(self): 
    
        '''
        get_categories gives a matrix, containing the name of each category and its link (in that order)
        '''
        
        _Start = "https://tivoneat.co.il/wp-content/themes/tivoneat/recLoad.php?paged=1&postsPerPage=6&category="  # begining of url for loading next page
        
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, 'html.parser')                          # getting the webpage
        
        category_recipes = []
        category_num = []
        
        sub_menu = soup.find(class_="sub-menu")                                    # getting the part with the recipes links
         
        for a in sub_menu.find_all('a', href=True):                                # getting the categories names and links
            page1 = requests.get(a['href'])                                        # weblink to a specific category
            soup1 = BeautifulSoup(page1.content, 'html.parser')
            body_id = str(soup1.find('body')).split(">")[0]                        # this part contains the category's number
            number_of_category = ''.join(filter(str.isdigit, body_id))             # extracting only the number itself
            category_recipes.append([[a.get_text()], a['href']])
            category_num.append(number_of_category)
            
        for i in range(len(category_recipes)):                                      # changing the url so we can load the whole recipes
            new_url = _Start+str(category_num[i])+"&lm=false"
            category_recipes[i][1] = new_url
            
        
        return category_recipes
    
    
    
    
    def _get_recipes(index):
        
        '''
        get_recipes gives all the links to the recipes for a specific category
        the category is chosen by its row index from the get_categories function
        '''
        
        category_recipes = Tivoneat._get_categories()                           # loads the matrix with the urls of the categories
        
        recipes_link = []
        
        url_load = category_recipes[index][1].split('&')                           # split the url so we can change sector
        url_load[0] = url_load[0][:-1]
        
        j = 1
        
        is_last = False
        
        while not is_last:
            url_load[0] = url_load[0]+str(j)                                       # next sector
            new_url = '&'.join(url_load)
            
            page = requests.get(new_url)
            soup = BeautifulSoup(page.content, 'html.parser') 
            
            for a in soup.find_all('a', href=True): 
                recipes_link.append(a['href'])                                     # adds the links in this sector of the category
        
            url_load = new_url.split('&')
            url_load[0] = url_load[0][:-1]
            
            j += 1
            is_last = eval(str(soup.find('script').get_text().split()[2][:-1]).capitalize())  # checks if we got the last page of the category, based on a script in the webpage itself
        
        
        return recipes_link
    
    
    
    def _get_ingredients(index):
        
        '''
        get_ingredients will give a list of ingredientes of every recipe in a specific category, next to the recipe's url
        the category is chosen by its row index from the get_categories function
        '''
        
        recipes_link = Tivoneat._get_recipes(index)
        
        recipe_ingr = []
        
        for i in range(len(recipes_link)):
            page = requests.get(recipes_link[i])
            soup = BeautifulSoup(page.content, 'html.parser') 
        
            relevent_part = soup.find(class_="recipeIng") # the class that contains the ingredients
        
            ingredients = relevent_part.get_text().split() # getting only the text into a list
            exclude_words = ['+','מה','צריך','חתיכות','גרם','קשה','כפית','כפות','על','פי','טעם','ציפוי','ראשון','שני','כוס','כמה','טיגון'] # irrelevant words that can be excluded
            final_ingredients = [x for x in ingredients if not (x.isdigit() or x=='/' or x in exclude_words)] # no digits or irrelevant symbols
            str_ingerdients = ' '.join(final_ingredients)
            values = [recipes_link[i], str_ingerdients]
            
            recipe_ingr.append(values)
        
        return recipe_ingr


'''
from here, we will work with a table created with MySQL, so first lets import it
'''
    




"""
category_from_index translate the number that the user will choose as its category, to the related categories in our table
"""
def category_from_index(i):
    if i == 1:
        sql_select_query = """SELECT URL, Ingredients FROM Ingredients_Table WHERE Category LIKE '%בוקר%'"""
        cursor.execute(sql_select_query)
        records = cursor.fetchall()
        return records
    if i == 2:
        sql_select_query = """SELECT URL, Ingredients FROM Ingredients_Table WHERE Category LIKE '%עיקריות%'"""
        cursor.execute(sql_select_query)
        records = cursor.fetchall()
        return records
    if i == 3:
        sql_select_query = """SELECT URL, Ingredients FROM Ingredients_Table WHERE Category LIKE '%קינוחים%'"""
        cursor.execute(sql_select_query)
        records = cursor.fetchall()
        return records
    if i == 4: 
        sql_select_query = """SELECT URL, Ingredients FROM Ingredients_Table WHERE Category LIKE '%סלטים%'"""
        cursor.execute(sql_select_query)
        records = cursor.fetchall()
        return records
    if i == 5: 
        sql_select_query = """SELECT URL, Ingredients FROM Ingredients_Table WHERE Category LIKE '%נשנושים%'"""
        cursor.execute(sql_select_query)
        records = cursor.fetchall()
        return records
    if i == 6:
        sql_select_query = """SELECT URL, Ingredients FROM Ingredients_Table WHERE Category LIKE '%שייקים%'"""
        cursor.execute(sql_select_query)
        records = cursor.fetchall()
        return records
    if i == 7:
        sql_select_query = """SELECT URL, Ingredients FROM Ingredients_Table WHERE Category LIKE '%גבינות%'"""
        cursor.execute(sql_select_query)
        records = cursor.fetchall()
        return records

'''
gluten function gives all the records related to no-gluten recipies 
'''


def gluten():
    sql_select_query = """SELECT URL, Ingredients FROM Ingredients_Table WHERE Category LIKE '%גלוטן%'"""
    cursor.execute(sql_select_query)
    no_gluten = cursor.fetchall()
    return no_gluten

'''
the search algorithm - first the user will choose the kind of recipe he's looking for
than he will input the restrictions
'''


def search():
    no_gluten = gluten()
    
    url_list = []
    usr_input = int(input("מהו סוג המתכון המבוקש? (הקש את המספר)\n1. ארוחות בוקר\n2. עיקריות \n3. קינוחים ומתוקים\n4. סלטים\n5. נשנושים וחטיפים\n6. שייקים ומשקאות\n7. גבינות וממרחים\n"))
    while usr_input not in range(1,8):
        usr_input = int(input("בחירה לא חוקית; אנא בחר שנית:\n1. ארוחות בוקר\n2. עיקריות\n3. קינוחים ומתוקים\n4. סלטים\n5. נשנושים וחטיפים\n6. שייקים ומשקאות\n7. גבינות וממרחים\n"))
    records = category_from_index(usr_input)
    
    
    restrictions = input("מהן המגבלות התזונתיות? (ניתן לבחור יותר מאחד, יש להקיש רווח בין בחירה לבחירה)\n")
    restrictionsList = restrictions.split()
    
    
    for url, ingr in records:
        if not all(x in ingr for x in restrictionsList):
            url_list.append(url)
    
    
    URLS = []
    for url, ingr in records:
        URLS.append(url)
    
    if 'גלוטן' in restrictionsList:    # if gluten is entered as restriction, algorithm will add the relevant recipes from the gluten cloumn in our table
        restrictionsList.remove('גלוטן')
        for url, ingr in no_gluten:
            if url in URLS:
                if not all(x in ingr for x in restrictionsList):
                    url_list.append(url) 
    return url_list   

#print(search())









