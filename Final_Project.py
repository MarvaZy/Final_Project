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


tivoneat = "https://tivoneat.co.il/"                                  # home page of one of the recipes' websites

'''
get_categories gives a matrix, containing the name of each category, its number and its link (in that order)
'''

def get_categories(url): 
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')                 # getting the webpage
    
    category_recipes = []
    
    sub_menu = soup.find(class_="sub-menu")                           # getting the part with the recipes links
     
    for a in sub_menu.find_all('a', href=True):                       # getting the categories names and links
        page1 = requests.get(a['href'])                               # weblink to a specific category
        soup1 = BeautifulSoup(page1.content, 'html.parser')
        body_id = str(soup1.find('body')).split(">")[0]               # this part contains the category's number
        number_of_category = ''.join(filter(str.isdigit, body_id))    # extracting only the number itself
        category_recipes.append([[a.get_text()],number_of_category, a['href']])
        
    for i in range(len(category_recipes)):                           # changing the url so we can load the whole recipes
        new_url = "https://tivoneat.co.il/wp-content/themes/tivoneat/recLoad.php?paged=1&postsPerPage=6&category="+str(category_recipes[i][1])+"&lm=false"
        category_recipes[i][2] = new_url
        
    
    return category_recipes

'''
get_recipes gives all the links to the recipes for a specific category.
the category is chosen by its row index from the get_categories function
'''


def get_recipes(i):
    category_recipes = get_categories(tivoneat)                     # loads the matrix with the urls of the categories
    
    recipes_link = []
    
    page = requests.get(category_recipes[i][2])
    soup = BeautifulSoup(page.content, 'html.parser') 
    isLast = eval(str(soup.find('script').get_text().split()[2][:-1]).capitalize())  # checks if we got the last page of the category, based on a script in the webpage itself
    
    for a in soup.find_all('a', href=True):                        # adds the links in this sector of the category
        recipes_link.append(a['href'])
    
    url_load = category_recipes[i][2].split('&')                   # split the url so we can change sector
    url_load[0] = url_load[0][:-1]
    
    j = 2
    
    
    while isLast == False:
        url_load[0] = url_load[0]+str(j)                          # next sector
        new_url = '&'.join(url_load)
        
        page = requests.get(new_url)
        soup = BeautifulSoup(page.content, 'html.parser') 
        
        for a in soup.find_all('a', href=True): 
            recipes_link.append(a['href'])
    
        url_load = category_recipes[i][2].split('&')
        url_load[0] = url_load[0][:-1]
        
        j += 1
        isLast = eval(str(soup.find('script').get_text().split()[2][:-1]).capitalize())
    
    return recipes_link
      
'''
get_ingredients will give a list of ingredientes of every recipe in a specific category, next to the recipe's url
the category is chosen by its row index from the get_categories function

'''


def get_ingredients(i):
    recipes_link = get_recipes(i)
    
    recipe_ingr = []
    
    for i in range(len(recipes_link)):
        page = requests.get(recipes_link[i])
        soup = BeautifulSoup(page.content, 'html.parser') 
    
        relevent_part = soup.find(class_="recipeIng") # the class that contains the ingredients
    
        Ingredients = relevent_part.get_text().split() # getting only the text into a list
        exclude_words = ['+','מה','צריך','חתיכות','גרם','קשה','כפית','כפות','על','פי','טעם','ציפוי','ראשון','שני','כוס','כמה','טיגון'] # irrelevant words that can be excluded
        final_ingredients = [x for x in Ingredients if not (x.isdigit() or x=='/' or x in exclude_words)] # no digits or irrelevant symbols
        str_ingerdients = ' '.join(final_ingredients)
        values = (recipes_link[i], str_ingerdients)
        
        recipe_ingr.append(values)
    
    return recipe_ingr


'''
next parts - not edited yet!
database + search algorithm

'''
    
#''''''''''''''''''''''''''''''''''''''''
import mysql.connector as mysql

db = mysql.connect(
    host = "localhost",
    user = "root",
    passwd = "123456789",
    database = "final_project"
)

cursor = db.cursor()


# =============================================================================
# query = "INSERT INTO ingredients_list (url_code, ing_list) VALUES (%s, %s)"
# ## storing values in a variable
# values = (url, str_ingerdients)
# 
# ## executing the query with values
# cursor.execute(query, values)
# 
# ## to make final output we have to run the 'commit()' method of the database object
# db.commit()
# 
# =============================================================================

query = "SELECT * FROM ingredients_list"

## getting records from the table
cursor.execute(query)

## fetching all records from the 'cursor' object
records = cursor.fetchall()

## Showing the data
for record in records:
    print(record)


#''''''''''''''''''''''''''''''''''''''''
#''''''''''''''''''''''''''''''''''''''''

# =============================================================================
# """
# The search algorithm
# """
# 
# usr_input = int(input("מהו סוג המתכון המבוקש? (הקש את המספר)\n1. ארוחת בוקר\n2.סלטים\n3. עיקריות\n4.קינוחים\n"))
# 
# 
# while usr_input not in range(1,5):
#     usr_input = input("בחירה לא חוקית; אנא בחר שנית:\n1. ארוחת בוקר\n2.סלטים\n3. עיקריות\n4.קינוחים\n")
#     
# restrictions = list(map(int, input("מהן המגבלות התזונתיות? (ניתן לבחור יותר מאחד, יש להקיש רווח בין בחירה לבחירה)\n1. רגישות לחלב\n2. רגישות לגלוטן\n3. צמחונות\n4. טבעונות\n5. אחר\n").split()))
# print(restrictions)
# #if usr_input == '1':
# #    search()
# #elif usr_input == '2':
#  #   sys.exit()
# =============================================================================

        
        
    
    
    
   
        
        
  


      
        
        