from BaseCrawler import BaseCrawler

class MarkivSodi(BaseCrawler):
    
    def __init__(self):
        self.url = "https://www.markivsodi.co.il/"
        self.category_class = "sub-menu"
        self.gluten_class = None
        self.posts_class = "archive-blog"
        self.header_type = "h3"
        self.button_class = None
        self.ingredients_class = "entry-content"
        self.table = None                                      
      
# loads all the data from the website to the DB
MarkivSodi = MarkivSodi()
MarkivSodi.insert_ingredients()