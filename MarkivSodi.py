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


class MarkivSodi(db):
    
    def __init__(self):
        super(MarkivSodi, self).__init__()
        # home page
        self.url = "https://www.markivsodi.co.il/"                             

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
        sub_menu = soup.find(class_="sub-menu")                                    
    
        # getting the categories names and links
        for a in sub_menu.find_all('a', href=True):                                
            all_categories.append([[a.get_text()], a['href']]) 
         
        url_list = []
        for i in [1,8,9,10]:
            url_list.append(all_categories[i][1])
        category_recipes['קינוחים ומתוקים'] = url_list
        
        category_recipes['נשנושים וחטיפים'] = [all_categories[7][1]]
        
        url_list = []
        for i in [13, 14, 16]:
            url_list.append(all_categories[i][1])
        category_recipes['עיקריות'] = url_list
            
        category_recipes['סלטים'] = [all_categories[15][1]]
        
        category_recipes['גבינות וממרחים'] = [all_categories[7][1]]
        
        category_recipes['נטול גלוטן'] = [all_categories[21][1]]
        
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
            # list of all the urls for the recipes in that category
            recipes_links = []
            # list of all the names for the recipes in that category
            recipes_names = []
            
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
                page1 = se.get(new_url)
                soup1 = BeautifulSoup(page1.content, 'html.parser')
                main_page = soup1.find(class_="archive-blog")
                for a in main_page.find_all('a', href=True):
                    if self.url in a['href'] and "comments" not in a['href'] and "respond" not in a['href']:
                        recipes_links.append(a['href'].strip())      
                # deletes duplicates of links
                recipes_links = list(dict.fromkeys(recipes_links))
                # the name of the recipe
                headers = main_page.find_all('h3') 
                for h in headers:
                    recipes_names.append(h.get_text())
                    
            # join the name of the recipe to its link
            for i in range(len(recipes_links)):
                recipes[recipes_names[i]] = {"url": recipes_links[i]}
        
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
            relevent_part = soup.find(class_="entry-content").get_text()                 
            try:
                relevent_part = relevent_part.split("לנו?")[1].split("אופן הכנה:")[0]
            except IndexError:
                try:
                    relevent_part = relevent_part.split("מרכיבים:")[1].split("אופן הכנה:")[0]
                # if relevant part doesnt contain "לנו?" or "מרכיבים:" there is something wrong with the url
                except IndexError:
                    print("Error, check "+recipe+" url: "+recipes_ingr[recipe])

            # getting only the text into a list
            ingredients = relevent_part.split()                                    
            exclude_words = ['מרכיבים','+','מה','צריך','חתיכות','גרם','קשה','כפית','כפות','על','פי','טעם','ציפוי','ראשון','שני','כוס','כמה','טיגון'] # irrelevant words that can be excluded
            # no digits or irrelevant symbols
            final_ingredients = [x for x in ingredients if not (x.isdigit() 
                                                                or x=='/' 
                                                                or x 
                                                                in exclude_words)] 
            str_ingredients = ' '.join(final_ingredients)
            recipes_ingr[recipe]["ingredients"] = str_ingredients
    
        return recipes_ingr
    
# insert all the data to the SQL table
markiv_sodi = MarkivSodi()
markiv_sodi.insert()
        