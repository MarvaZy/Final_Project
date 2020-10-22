# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 15:20:13 2020

@author: MarvaZychlinski
"""
'''
For Veg Website Only
'''
from BaseCrawler import BaseCrawler

class Veg(BaseCrawler):
    
    def __init__(self):
        self.url = "https://veg.co.il/recipes/"
        self.category_class = "subcategories-as-images"
        self.gluten_class = "footer-extra-menu"
        self.posts_class = "archive-posts"
        self.header_type = "h3"
        self.button_class = "veg-button"
        self.ingredients_class = "ingredients"
        self.table = None 
 
# loads all the data from the website to the DB
Veg = Veg()
Veg.fetch_recipes()  
