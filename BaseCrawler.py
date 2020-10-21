# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 13:06:55 2020

@author: MarvaZychlinski
"""

from bs4 import BeautifulSoup
# in this website, we need to use selenium to click "load more" button
from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager
import requests
# this is to avoid getting blocked by the website
with requests.Session() as se:
    se.headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
        "Accept-Encoding": "gzip, deflate",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en"
    }
from db import db

class BaseCrawler():
    '''
    
    '''
    category_dictionary = {1: {"English": "Breakfast", "Hebrew": "ארוחות בוקר"}, 
                                    2: {"English": "MainCourse", "Hebrew": "עיקריות"}, 
                                    3: {"English": "Dessert", "Hebrew": "קינוחים ומתוקים"},
                                    4: {"English": "Salad", "Hebrew": "סלטים"},
                                    5: {"English": "Snack", "Hebrew": "נשנושים וחטיפים"},
                                    6: {"English": "Shake", "Hebrew": "שייקים ומשקאות"},
                                    7: {"English": "Spread", "Hebrew": "גבינות וממרחים"},
                                    8: {"English": "Gluten", "Hebrew": "נטול גלוטן"}                    
                                    }
    
    def __init__(self):
        # home page
        self.url = None
        self.category_class = None
        self.gluten_class = None
        self.posts_class = None
        self.header_type = None
        self.button_class = None
        self.ingredients_class = None
        self.table = None
 
    def _get_categories(self):
        '''
        get_categories gives a dictionary, connecting between the name of each category (key) to its link (value)
        '''
        # getting the webpage
        page = se.get(self.url)
        soup = BeautifulSoup(page.content, 'html.parser')                          
        category_recipes = {BaseCrawler.category_dictionary[i]["Hebrew"]: [] for i in BaseCrawler.category_dictionary.keys()}
        gluten = False
        
        # getting the part with the recipes links
        sub_menu = soup.find('ul', class_=self.category_class)                                     
        # getting the categories names and links
        for a in sub_menu.find_all('a', href=True):
            # Consolidates categories from the site into predefined categories
            if any(word in a.get_text() for word in ["בוקר"]):    
                category_recipes['ארוחות בוקר'].append(a['href'])
            elif any(word in a.get_text() for word in ["עיקרי", "צהריים", "ערב", "משפחתית", "מרקים", "פסטות", "תבשילים", "קציצות", "ממולאים", "פשטידות", "מוקפצים", "ירקות"]):
                category_recipes['עיקריות'].append(a['href'])
            elif any(word in a.get_text() for word in ["קינוח", "עוגות"]):
                category_recipes['קינוחים ומתוקים'].append(a['href'])
            elif any(word in a.get_text() for word in ["סלטים"]):
                category_recipes['סלטים'].append(a['href'])
            elif any(word in a.get_text() for word in ["נשנוש", "חטי", "עוגיות"]):
                category_recipes['נשנושים וחטיפים'].append(a['href'])
            elif any(word in a.get_text() for word in ["שייק", "משקאות"]):
                category_recipes['שייקים ומשקאות'].append(a['href'])
            elif any(word in a.get_text() for word in ["גבינ", "ממרח", "מטבל"]):
                category_recipes['גבינות וממרחים'].append(a['href'])
            elif any(word in a.get_text() for word in ["גלוטן"]):
                gluten = True
                category_recipes['נטול גלוטן'].append(a['href'])
        
        # getting the part with the gluten-free recipes link
        if not gluten:
            sub_menu = soup.find(class_=self.gluten_class)                                             
            for a in sub_menu.find_all('a', href=True):
                if "גלוטן" in a.get_text():
                    category_recipes['נטול גלוטן'].append(a['href'])

        return category_recipes
    
    def _handleLoadMore(self, category):
        '''
        _handleLoadMore gives a nested dictionary connecting the recipes names to their urls for a specific category
        the category is chosen by key values from the get_categories function
        method of scrapping: clicking a "load more" button
        '''
        category_recipes = self._get_categories()
        recipes = {}
        # initializing a Chrome driver
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        driver = webdriver.Chrome(ChromeDriverManager().install())
        for url in category_recipes[category]:
            # only for Veg website
            if "http" not in url:
                url = self.url.split("/recipes/")[0] + url
            driver.get(url)
            # click load more button, if it exsits
            try:
                load_more = driver.find_element_by_class_name(self.button_class)
                while load_more.is_displayed():
                      driver.execute_script("arguments[0].click();", load_more)
                      time.sleep(4)
            except:
                pass
            soup = BeautifulSoup(driver.page_source, "lxml") 
            posts = soup.find(class_=self.posts_class)
            # getting recipes names and urls
            for post in posts.find_all('a', href=True):
                # deleting links to pages of collections of recipes
                if "אוסף" not in post.get_text():                            
                    recipes[post.find(self.header_type).get_text()] = {"url": post['href']}
           
        return recipes 
    
    def _handleNextPage(self, category):
        '''
        _handleNextPage gives a nested dictionary connecting the recipes names to their urls for a specific category
        the category is chosen by key values from the get_categories function
        method of scrapping: loading next url for more recipes
        '''
        category_recipes = self._get_categories()
        recipes = {}
        for url in category_recipes[category]: 
            page = se.get(url)
            soup = BeautifulSoup(page.content, 'html.parser') 
        
            # finds number of pages in the category, so we can load them 
            web_numbers = soup.find_all(class_="page-numbers")                         
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
                main_page = soup1.find(class_=self.posts_class)
                headers = main_page.find_all(self.header_type)
                for header in headers:
                    # deleting links to pages of collections of recipes
                    if "אוסף" not in header.get_text():
                        recipes[header.get_text()] = {"url": header.find('a', href=True)['href']}
        
        return recipes
    
    def _get_recipes(self, category):
        '''
        get_recipes gives a nested dictionary connecting the recipes names to their urls for a specific category
        the category is chosen by key values from the get_categories function
        '''                             
        if self.button_class:
            recipes = self._handleLoadMore(category)
            
        else:
            recipes = self._handleNextPage(category)

        return recipes
    
    def remove_non_alphanumeric(self, list_of_strings):
        '''
        removes all non alphanumeric characters from a list of strings
        '''
        non_alpha = []
        for word in list_of_strings:
            alphanumeric_filter = filter(str.isalnum, word)
            non_alpha.append("".join(alphanumeric_filter))
        
        return non_alpha
    
    def _get_ingredients(self, category):
        '''
        get_ingredients will give a nested dictionary for each recipe name, with its url and list of ingredientes
        the category is chosen by key values from the get_categories function
        '''
        recipes_ingr = self._get_recipes(category)
        for recipe in recipes_ingr:
            page = se.get(recipes_ingr[recipe]["url"])
            soup = BeautifulSoup(page.content, 'html.parser') 
            
            # the class that contains the ingredients - if table for ingredients exists or not, gets the relevent part
            if self.table: 
                pre = soup.find(class_=self.ingredients_class).find_all('pre')
                for i in range(len(pre)):
                    if "רכיבים" in pre[i].get_text():
                        relevent_part = pre[i].get_text()
            else:
                relevent_part = soup.find(class_=self.ingredients_class).get_text()     
            
            try:
                relevent_part = relevent_part.split("לנו?")[1].split("אופן הכנה:")[0]
            except IndexError:
                try:
                    relevent_part = relevent_part.split("מרכיבים:")[1].split("אופן הכנה:")[0]
                # if relevant part doesnt contain "לנו?" or "מרכיבים:" there is something wrong with the url
                except:
                    pass
            except:
                pass
                    
            # getting only the text into a list
            ingredients = relevent_part.split() 
            # irrelevant words that can be excluded
            exclude_words = ['+','מה','צריך','חתיכות','גרם','קשה','כפית','כפות','על','פי','טעם','ציפוי','ראשון','שני','כוס','כמה', 'מרכיבים', 'טיגון'] 
            # no digits or irrelevant symbols
            final_ingredients = self.remove_non_alphanumeric([x for x in ingredients if not 
                                                               (x.isdigit() 
                                                                or x=='/' 
                                                                or x in exclude_words)])
            str_ingredients = ' '.join(final_ingredients)
            recipes_ingr[recipe]["ingredients"] = str_ingredients
        
        return recipes_ingr
    
    def insert_ingredients(self):
        DB = db()
        for index in BaseCrawler.category_dictionary.keys():
            eng_category = BaseCrawler.category_dictionary[index]["English"]
            heb_category = BaseCrawler.category_dictionary[index]["Hebrew"]
            ingr_dictionary = self._get_ingredients(heb_category)
            DB.bulk_insert(eng_category, ingr_dictionary)
        
        return 
            
            
