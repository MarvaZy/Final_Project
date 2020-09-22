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
        # home page of Tivoneat websites
        self.url = "https://tivoneat.co.il/"                                   
 
    def _get_categories(self): 
    
        '''
        get_categories gives a matrix, containing the name of each category and its link (in that order)
        '''
        
        # begining of url for loading next page
        _Start = "https://tivoneat.co.il/wp-content/themes/tivoneat/recLoad.php?paged=1&postsPerPage=6&category="  
        
        # getting the webpage
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, 'html.parser')                          
        
        category_recipes = []
        
        # getting the part with the recipes links
        sub_menu = soup.find(class_="sub-menu")                                    
         
        # getting the categories names and links
        for a in sub_menu.find_all('a', href=True):                                
            # weblink to a specific category
            page1 = requests.get(a['href'])                                        
            soup1 = BeautifulSoup(page1.content, 'html.parser')
            
            # this part contains the category's number
            body_id = str(soup1.find('body')).split(">")[0]                        
            # extracting only the number itself
            number_of_category = str(''.join(filter(str.isdigit, body_id)))
            
            # changing the url so we can load the whole recipes
            new_url = _Start+number_of_category+"&lm=false"
            category_recipes.append([[a.get_text()], new_url])
            
        return category_recipes
    
    def _get_recipes(index):
        
        '''
        get_recipes gives all the links to the recipes for a specific category
        the category is chosen by its row index from the get_categories function
        '''
        
        # loads the matrix with the urls of the categories
        category_recipes = Tivoneat._get_categories()                           
        
        recipes_link = []
        
        # split the url so we can change sector
        url_load = category_recipes[index][1].split('&')                           
        url_load[0] = url_load[0][:-1]
        
        j = 1
        
        is_last = False
        
        while not is_last:
            # next sector
            url_load[0] = url_load[0]+str(j)                                       
            new_url = '&'.join(url_load)
            
            page = requests.get(new_url)
            soup = BeautifulSoup(page.content, 'html.parser') 
            
            for a in soup.find_all('a', href=True): 
                # adds the links in this sector of the category
                recipes_link.append(a['href'])                                     
        
            url_load = new_url.split('&')
            url_load[0] = url_load[0][:-1]
            
            j += 1
            # checks if we got the last page of the category, based on a script in the webpage itself
            is_last = eval(str(soup.find('script').get_text().split()[2][:-1]).capitalize())  
                
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
        
            # the class that contains the ingredients
            relevent_part = soup.find(class_="recipeIng") 
        
            # getting only the text into a list
            ingredients = relevent_part.get_text().split() 
            # irrelevant words that can be excluded
            exclude_words = ['+','מה','צריך','חתיכות','גרם','קשה','כפית','כפות','על','פי','טעם','ציפוי','ראשון','שני','כוס','כמה','טיגון'] 
            # no digits or irrelevant symbols
            final_ingredients = [x for x in ingredients if not (x.isdigit() 
                                                                or x=='/' 
                                                                or x 
                                                                in exclude_words)] 
            str_ingerdients = ' '.join(final_ingredients)
            values = [recipes_link[i], str_ingerdients]
            
            recipe_ingr.append(values)
        
        return recipe_ingr
