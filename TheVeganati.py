# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 14:04:33 2020

@author: MarvaZychlinski
"""

'''
For TheVeganati Website Only
'''

from db import db
import requests
from bs4 import BeautifulSoup

# this is to avoid getting blocked by the website
with requests.Session() as se:
    se.headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
        "Accept-Encoding": "gzip, deflate",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en"
    }

class TheVeganati(db):
    
    def __init__(self):
        super(TheVeganati, self).__init__()
        # home page
        self.url = "https://theveganati.com/"                                   
 
    def _get_categories(self): 
        
        '''
        get_categories gives a dictionary, connecting between the name of each category (key) to its link (value)
        '''
        
        # getting the webpage
        page = se.get(self.url)
        soup = BeautifulSoup(page.content, 'html.parser')                          
        
        category_recipes = {}
        all_categories = []
        
        # getting the part with the recipes links
        sub_menu = soup.find('ul', class_="sub-menu")                                    
         
        # getting the categories names and links
        for a in sub_menu.find_all('a', href=True):                                
            all_categories.append([[a.get_text()], a['href']])
        
        # getting the part with the gluten-free recipes link
        sub_menu = soup.find(class_="tagcloud")                                             
        for a in sub_menu.find_all('a', href=True):
            if "גלוטן" in a.get_text():
                all_categories.append([[a.get_text()], a['href']])
        
        category_recipes['ארוחות בוקר'] = [all_categories[0][1]]
        
        url_list = []
        for i in [1,2,3]:
            url_list.append(all_categories[i][1])
        category_recipes['עיקריות'] = url_list
        
        category_recipes['קינוחים ומתוקים'] = all_categories[4][1]
        
        url_list = []
        for i in [6,7]:
            url_list.append(all_categories[i][1])
        category_recipes['נשנושים וחטיפים'] = url_list
        
        category_recipes['סלטים'] = [all_categories[8][1]]
        
        category_recipes['נטול גלוטן'] = [all_categories[10][1]]
            
        return category_recipes
    
    def _get_recipes(self, category):
        
        '''
        get_recipes gives a nested dictionary connecting the recipes names to their urls for a specific category
        the category is chosen by key values from the get_categories function
        '''
        
        # loads the dictionary with the urls of the categories
        category_recipes = self._get_categories()                              
        recipes = {}
        
        for url in category_recipes[category]:
            page = se.get(url)
            soup = BeautifulSoup(page.content, 'html.parser') 
        
            # finds number of pages in the category, so we can load them 
            web_numbers = soup.find_all('a', class_="page-numbers")                         
            page_numbers = []
            for a in web_numbers:
                if a.get_text().isdigit():
                    page_numbers.append(a.get_text())  
            if len(page_numbers) > 0:
                page_numbers = int(page_numbers[-1])
            else:
                page_numbers = 1
               
            # getting the recipes links and names
            for i in range(1,page_numbers+1):
                new_url = url+"page/"+str(i)+"/"
                page1 = se.get(new_url, verify=False)
                soup1 = BeautifulSoup(page1.content, 'html.parser')
                main_page = soup1.find(class_="posts-wrap")
                headers = main_page.find_all('h3', class_="entry-title")
                for i in range(len(headers)):
                    for a in headers[i].find_all('a', href=True):
                        recipes[a.get_text()] = {"url": a['href']}
                      
        # deleting links to pages of collections of recipes
        for recipe in recipes.copy():
            if "אוסף" in str(recipe):
                del(recipes[recipe])
            
        return recipes
    
    def _get_ingredients(self, category):
        
        '''
        get_ingredients will give a nested dictionary for each recipe name, with its url and list of ingredientes
        the category is chosen by key values from the get_categories function
        '''
        global relvent_part
        recipes_ingr = self._get_recipes(category)
        for recipe in recipes_ingr:
            page = se.get(recipes_ingr[recipe]["url"])
            soup = BeautifulSoup(page.content, 'html.parser') 
            # the class that contains the ingredients
            pre = soup.find(class_="entry-content").find_all('pre')
            for i in range(len(pre)):
                if "רכיבים" in pre[i].get_text():
                    relevent_part = pre[i]
            
            # getting only the text into a list
            ingredients = relevent_part.get_text().split() 
            # irrelevant words that can be excluded
            exclude_words = ['+','מה','צריך','חתיכות','גרם','קשה','כפית','כפות','על','פי','טעם','ציפוי','ראשון','שני','כוס','כמה', 'רכיבים:', 'טיגון'] 
            # no digits or irrelevant symbols
            final_ingredients = [x for x in ingredients if not (x.isdigit() 
                                                                or x=='/' 
                                                                or x 
                                                                in exclude_words)] 
            str_ingredients = ' '.join(final_ingredients)
            recipes_ingr[recipe]["ingredients"] = str_ingredients
        
        return recipes_ingr

# insert all the data to the SQL table
the_veganati = TheVeganati()
the_veganati.insert()