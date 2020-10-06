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
        get_categories gives a dictionary, connecting between the name of each category (key) to its link (value)
        '''
        
        # begining of url for loading next page
        _start = "https://tivoneat.co.il/wp-content/themes/tivoneat/recLoad.php?paged=1&postsPerPage=6&category="  
        
        # getting the webpage
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, 'html.parser')                          
        
        category_recipes = {}
        
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
            new_url = _start+number_of_category+"&lm=false"
            category_recipes[a.get_text()] = str(new_url)
            
        return category_recipes
    
    def _get_recipes(self, category):
        
        '''
        get_recipes gives a nested dictionary connecting the recipes names to their urls for a specific category
        the category is chosen by key values from the get_categories function
        '''
        
        # loads the dictionary with the urls of the categories
        category_recipes = self._get_categories()                           
        
        # list of all the urls for the recipes in that category
        recipes_links = []
        # list of all the names for the recipes in that category
        recipes_names = []
        
        # split the url so we can change sector
        url_load = category_recipes[category].split('&')                           
        
        j = 1
        
        is_last = "False"
        
        while is_last == "False":
            # next sector
            url_load[0] = ''.join(url_load[0].split('=')[0]) + "=" + str(j)                                       
            new_url = '&'.join(url_load)
            
            page = requests.get(new_url)
            soup = BeautifulSoup(page.content, 'html.parser') 
            
            for a in soup.find_all('a', href=True): 
                # adds the links in this sector of the category
                recipes_links.append(a['href'])                                     
        
            # the name of the recipe
            headers = soup.find_all('h2')
            for h in headers:
                recipes_names.append(h.get_text())
            
            # preparing for next page
            url_load = new_url.split('&')
            
            j += 1
            # checks if we got the last page of the category, based on a script in the webpage itself
            is_last = str(soup.find('script').get_text().split()[2][:-1]).capitalize()  
                
        # join the name of the recipe to its link
        recipes = {}
        for i in range(len(recipes_links)):
            recipes[recipes_names[i]] = {"url": recipes_links[i]}
        
        return recipes
    
    def get_ingredients(self, category):
        
        '''
        get_ingredients will give a nested dictionary for each recipe name, with its url and list of ingredientes
        the category is chosen by key values from the get_categories function
        '''
        
        recipes_ingr = self._get_recipes(category)
        for recipe in recipes_ingr:
            page = requests.get(recipes_ingr[recipe]["url"])
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
            str_ingredients = ' '.join(final_ingredients)
            recipes_ingr[recipe]["ingredients"] = str_ingredients
        
        return recipes_ingr