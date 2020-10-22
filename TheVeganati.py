# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 14:04:33 2020

@author: MarvaZychlinski
"""

'''
For TheVeganati Website Only
'''

from BaseCrawler import BaseCrawler

class TheVeganati(BaseCrawler):
    
    def __init__(self):
        self.url = "https://theveganati.com/"
        self.category_class = "sub-menu"
        self.gluten_class = "tagcloud"
        self.posts_class = "posts-wrap"
        self.header_type = "h3"
        self.button_class = None
        self.ingredients_class = "entry-content"
        self.table = True                                   
 
# loads all the data from the website to the DB
TheVeganati = TheVeganati()
TheVeganati.fetch_recipes() 