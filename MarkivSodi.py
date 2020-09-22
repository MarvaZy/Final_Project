import requests
from bs4 import BeautifulSoup
with requests.Session() as se:
    se.headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
        "Accept-Encoding": "gzip, deflate",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en"
    }



class MarkivSodi:
    
    def __init__(self):
        self.url = "https://www.markivsodi.co.il/"                             # home page of one of the recipes' websites



def _get_categories(self): 
    
    '''
    get_categories gives a matrix, containing the name of each category and its link (in that order)
    '''
    
    page = se.get(self.url)
    soup = BeautifulSoup(page.content, 'html.parser')                          # getting the webpage
    
    category_recipes = []
    all_categories = []

    
    sub_menu = soup.find(class_="sub-menu")                                    # getting the part with the recipes links

    for a in sub_menu.find_all('a', href=True):                                # getting the categories names and links
        all_categories.append([[a.get_text()], a['href']]) 
     
    for i in [1,8,9,10]:
        category_recipes.append(['קינוחים ומתוקים', all_categories[i][1]])
    
    category_recipes.append(['נשנושים וחטיפים', all_categories[7][1]])
    
    for i in [13, 14, 16]:
        category_recipes.append(['עיקריות', all_categories[i][1]])
        
    category_recipes.append(['סלטים', all_categories[15][1]])
    
    category_recipes.append(['גבינות וממרחים', all_categories[7][1]])
    
    category_recipes.append(['נטול גלוטן', all_categories[21][1]])
    
    
    return category_recipes



def _get_recipes(self, index):
    
    '''
    get_recipes gives all the links to the recipes for a specific category
    the category is chosen by its row index from the get_categories function
    '''
    
    category_recipes = _get_categories(self.url)                              # loads the matrix with the urls of the categories
    
    recipes_link = []
    
    page = se.get(category_recipes[index][1])
    soup = BeautifulSoup(page.content, 'html.parser') 

    web_numbers = soup.find_all(class_="page-numbers")                         # getting the part with the recipes links
    page_numbers = []
    
    for a in web_numbers:
        if a.get_text().isdigit():
            page_numbers.append(a.get_text())

    if len(page_numbers) > 0:
        page_numbers = int(page_numbers[-1])
    else:
        page_numbers = 1

       
    for i in range(1,page_numbers+1):
        new_url = category_recipes[index][1]+"page/"+str(i)+"/"
        page1 = se.get(new_url)
        soup1 = BeautifulSoup(page1.content, 'html.parser')
        main_page = soup1.find(class_="archive-blog")

        for a in main_page.find_all('a', href=True):
            if self.url in a['href'] and "comments" not in a['href'] and "respond" not in a['href']:
                recipes_link.append(a['href'].strip())

    recipes_link = list(dict.fromkeys(recipes_link))
    
    return recipes_link



def _get_ingredients(index):
    
    '''
    get_ingredients will give a list of ingredientes of every recipe in a specific category, next to the recipe's url
    the category is chosen by its row index from the get_categories function
    '''
    
    recipes_link = _get_recipes(index)
    
    recipe_ingr = []
    
    for i in range(len(recipes_link)):
        page = se.get(recipes_link[i])
        soup = BeautifulSoup(page.content, 'html.parser') 
    
        relevent_part = soup.find(class_="entry-content")                      # the class that contains the ingredients
        relevent_part = relevent_part.get_text().split("אז מה היה לנו?")[1].split("אופן הכנה:")[0]
        Ingredients = relevent_part.split()                                    # getting only the text into a list
        exclude_words = ['מרכיבים','+','מה','צריך','חתיכות','גרם','קשה','כפית','כפות','על','פי','טעם','ציפוי','ראשון','שני','כוס','כמה','טיגון'] # irrelevant words that can be excluded
        final_ingredients = [x for x in Ingredients if not (x.isdigit() 
                                                            or x=='/' 
                                                            or x 
                                                            in exclude_words)] # no digits or irrelevant symbols
        str_ingerdients = ' '.join(final_ingredients)
        values = [recipes_link[i], str_ingerdients]
        
        recipe_ingr.append(values)
    
    return recipe_ingr


print(_get_ingredients(4))


    