# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 20:22:12 2020

@author: MarvaZychlinski
"""

'''
For Tivoneat Website Only
'''

from BaseCrawler import BaseCrawler

class Tivoneat(BaseCrawler):
    
    def __init__(self):
        self.url = "https://tivoneat.co.il/" 
        self.category_class = "sub-menu"
        self.gluten_class = None
        self.posts_class = "postsList"
        self.header_type = "h2"
        self.button_class = "moreRecipesBtn"
        self.ingredients_class = "recipeIng"
        self.table = None                                        
 
# loads all the data from the website to the DB
Tivoneat = Tivoneat()
Tivoneat.insert_ingredients()

