
import requests
from bs4 import BeautifulSoup


url = "https://tivoneat.co.il/schnitzel/" # prototype

page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser') # getting the webpage of the specific recipie


relevent_part = soup.find(class_="recipeIng") # for each website - different class name to be found

Ingredients = relevent_part.get_text().split() # getting only the text into a list
exclude_words = ['מה','צריך','חתיכות','גרם','קשה','כפית','כפות','על','פי','טעם','ציפוי','ראשון','שני','כוס','כמה','טיגון'] # irrelevant words that can be excluded
final_ingredients = [x for x in Ingredients if not (x.isdigit() or x=='/' or x in exclude_words)] # no digits or irrelevant symbols
str_ingerdients = ' '.join(final_ingredients)
#''''''''''''''''''''''''''''''''''''''''
import mysql.connector as mysql

db = mysql.connect(
    host = "localhost",
    user = "root",
    passwd = "123456789",
    database = "final_project"
)

cursor = db.cursor()


# =============================================================================
# query = "INSERT INTO ingredients_list (url_code, ing_list) VALUES (%s, %s)"
# ## storing values in a variable
# values = (url, str_ingerdients)
# 
# ## executing the query with values
# cursor.execute(query, values)
# 
# ## to make final output we have to run the 'commit()' method of the database object
# db.commit()
# 
# =============================================================================

query = "SELECT * FROM ingredients_list"

## getting records from the table
cursor.execute(query)

## fetching all records from the 'cursor' object
records = cursor.fetchall()

## Showing the data
for record in records:
    print(record)


#''''''''''''''''''''''''''''''''''''''''
#''''''''''''''''''''''''''''''''''''''''

# =============================================================================
# """
# The search algorithm
# """
# 
# usr_input = int(input("מהו סוג המתכון המבוקש? (הקש את המספר)\n1. ארוחת בוקר\n2.סלטים\n3. עיקריות\n4.קינוחים\n"))
# 
# 
# while usr_input not in range(1,5):
#     usr_input = input("בחירה לא חוקית; אנא בחר שנית:\n1. ארוחת בוקר\n2.סלטים\n3. עיקריות\n4.קינוחים\n")
#     
# restrictions = list(map(int, input("מהן המגבלות התזונתיות? (ניתן לבחור יותר מאחד, יש להקיש רווח בין בחירה לבחירה)\n1. רגישות לחלב\n2. רגישות לגלוטן\n3. צמחונות\n4. טבעונות\n5. אחר\n").split()))
# print(restrictions)
# #if usr_input == '1':
# #    search()
# #elif usr_input == '2':
#  #   sys.exit()
# =============================================================================
