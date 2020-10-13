# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 15:20:13 2020

@author: MarvaZychlinski
"""
'''
For Veg Website Only
'''
from db import db
import requests
from bs4 import BeautifulSoup
# in this website, we need to use selenium to click "load more" button
from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager

# this is to avoid getting blocked by the website
with requests.Session() as se:
    se.headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
        "Accept-Encoding": "gzip, deflate",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en"
    }

class Veg(db):
    
    def __init__(self):
        super(Veg, self).__init__()
        # home page
        self.url = "https://veg.co.il/recipes/" 
        # initializing a Chrome driver
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--ignore-certificate-errors')
        self.driver = webdriver.Chrome(ChromeDriverManager().install())                                  
 
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
        sub_menu = soup.find('ul', class_="subcategories-as-images")                                     
        # getting the categories names and links
        for a in sub_menu.find_all('a', href=True):                                
            all_categories.append([[a.get_text()], self.url.split("/recipes/")[0]+a['href']])      
        
        # getting the part with the gluten-free recipes link
        sub_menu = soup.find('nav', class_="footer-extra-menu")                                             
        for a in sub_menu.find_all('a', href=True):
            if "גלוטן" in a.get_text():
                all_categories.append([[a.get_text()], a['href']])  
        
        # Consolidates categories from the site into predefined categories
        category_recipes['ארוחות בוקר'] = [all_categories[0][1]]      
        category_recipes['סלטים'] = [all_categories[1][1]]     
        url_list = []
        for i in [2,3,4,6,9,10,11,12,13,17]:
            url_list.append(all_categories[i][1])
        category_recipes['עיקריות'] = url_list  
        url_list = []
        for i in [5,14,15]:
            url_list.append(all_categories[i][1])
        category_recipes['קינוחים ומתוקים'] = url_list   
        category_recipes['גבינות וממרחים'] = [all_categories[7][1]]
        category_recipes['נשנושים וחטיפים'] = [all_categories[8][1]]
        category_recipes['שייקים ומשקאות'] = all_categories[16][1]
        category_recipes['נטול גלוטן'] = [all_categories[18][1]]
            
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
            self.driver.get(url)
            # click load more button, if it exsits
            try:
                load_more = self.driver.find_element_by_class_name("veg-button")
                while load_more.is_displayed():
                      self.driver.execute_script("arguments[0].click();", load_more)
                      time.sleep(1)
            except:
                pass
            soup = BeautifulSoup(self.driver.page_source, "lxml") 
            posts = soup.find(class_="archive-posts")
            # getting recipes names and urls
            for post in posts.find_all('a', href=True):                           
                recipes[post.find('h3').get_text()] = {"url": post['href']}
               
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
        recipes_ingr = self._get_recipes(category)
        for recipe in recipes_ingr:
            page = se.get(recipes_ingr[recipe]["url"])
            soup = BeautifulSoup(page.content, 'html.parser') 
            # the class that contains the ingredients
            relevent_part = soup.find(class_="ingredients")     
            # getting only the text into a list
            ingredients = relevent_part.get_text().split() 
            # irrelevant words that can be excluded
            exclude_words = ['+','מה','צריך','חתיכות','גרם','קשה','כפית','כפות','על','פי','טעם','ציפוי','ראשון','שני','כוס','כמה', 'מרכיבים', 'טיגון'] 
            # no digits or irrelevant symbols
            final_ingredients = [x for x in ingredients if not (x.isdigit() 
                                                                or x=='/' 
                                                                or x 
                                                                in exclude_words)] 
            str_ingredients = ' '.join(final_ingredients)
            recipes_ingr[recipe]["ingredients"] = str_ingredients
        
        return recipes_ingr

# insert all the data to the SQL table
veg = Veg()
veg.insert()
