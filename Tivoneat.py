# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 20:22:12 2020

@author: MarvaZychlinski
"""

'''
For Tivoneat Website Only
'''

from BaseCrawler import BaseCrawler

class Tivoneat():
    
    def __init__(self):
        # home page
        self.url = "https://tivoneat.co.il/" 
        self.website = BaseCrawler(self.url)                                       
 
    def _get_categories(self): 
        '''
        get_categories gives a dictionary, connecting between the name of each category (key) to its link (value)
        '''
        category_class = "sub-menu"
        gluten_class = None
        category_recipes = self.website._get_categories(category_class, gluten_class)
            
        return category_recipes
    
    def _get_recipes(self, category):
        '''
        get_recipes gives a nested dictionary connecting the recipes names to their urls for a specific category
        the category is chosen by key values from the get_categories function
        '''
        # loads the dictionary with the urls of the categories
        category_recipes = self._get_categories()  
        posts_class = "postsList"
        header_type = "h2"
        button_class = "moreRecipesBtn"
        recipes = self.website._get_recipes(category_recipes, category, posts_class, header_type, button_class)
        
        return recipes
    
    def _get_ingredients(self, category):
        '''
        get_ingredients will give a nested dictionary for each recipe name, with its url and list of ingredientes
        the category is chosen by key values from the get_categories function
        '''
        recipes = self._get_recipes(category)
        ingredients_class = "recipeIng"
        table = None
        recipes_ingr = self.website._get_ingredients(recipes, ingredients_class, table)
        
        return recipes_ingr

