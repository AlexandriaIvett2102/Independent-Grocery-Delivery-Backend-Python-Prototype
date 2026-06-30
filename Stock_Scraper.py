# To make this work, you will need to inspect the class names of each vendor's HTML and input them into the list options lower on the page. But the bones are there

import requests
from bs4 import BeautifulSoup
import time

# CREATES CLASS FOR NUTRITION INFO - DECIDED TO BE BEST INSTEAD OF PARSING AS STRINGS AND REFORMATTING - MAKES PRESENTATION OF RESULTS SIMPLER
class NutritionInfo:
    def __init__(self, kcal, protein, carbs, sugars, fat, fibre, salt, vegetarian, vegan, allergens, ingredients):
        self.kcal = kcal
        self.protein = protein
        self.carbs = carbs 
        self.sugars = sugars 
        self.fat = fat 
        self.fibre = fibre 
        self.salt = salt
        self.vegetarian = vegetarian 
        self.vegan = vegan 
        self.allergens = allergens 
        self.ingredients = ingredients

    def __str__(self):
        return f"nutrition_info(kcal = {self.kcal}, protein = {self.protein}, carbs = {self.carbs}, sugars = {self.sugars}, fat = {self.fat}, fibre = {self.fibre}, salt ={self.salt}, vegetarian = {self.vegetarian}, vegan = {self.vegan}, allergens = {self.allergens}, ingredients = {self.ingredients})"      

# CREATES PRODUCT CLASS TO MAKE RECORDING OF NECESSARY INFO EASIER 
# USES PIC_URL AS LIVE LINK TO LOOPHOLE AROUND COPYWRITE LAWS OF PICTURES, NO COPYWRITE OF LIVE LINKS - DO NOT USE IMGUR, UNAVAILABLE IN UK         
class Product: 
    def __init__(self, name, brand, price, availability, product_type, vendor, nutrition_info, pic_url):
        self.name = name 
        self.brand = brand 
        self.price = price 
        self.availability = availability 
        self.product_type = product_type 
        self.vendor = vendor 
        self.nutrition_info = nutrition_info
        self.pic_url = pic_url 

    def __str__(self):
        return f"Product(name = {self.name}, brand = {self.brand}, price = {self.price}, availability = {self.availability}, product_type = {self.product_type}, vendor = {self.vendor}, nutrition_info = {self.nutrition_info}, pic_url = {self.pic_url})"
    
# PRODUCT MANAGER CLASS, ALLOWS FOR THE INTERACTION OF PRODUCTS IN THE SITE - VERY SELF-EXPLANATORY
class ProductManager:
    def __init__(self):
        self.products = {}
        self.next_id = 1

    def add_product(self, name, brand, price, availability, product_type, vendor, nutrition_info, pic_url):
        product_id = f"product_{self.next_id:03d}" 
        self.products [product_id] = Product (name, brand, price, availability, product_type, vendor, nutrition_info, pic_url)
        self.next_id += 1

    def remove_product(self, product_id):
        if product_id not in self.products:
            raise ValueError("Product does not exist")
        del self.products [product_id]
        print (f"Product '{product_id}' no-longer available")

    def display_products_all(self):
        if not self.products:
            print("No stock available")
        else:
            for products in self.products.values():
                print(products)
    
    def display_by_vendor(self, vendor):
        if not self.products:
            print("No Stock Available")
        else:
            for product in self.products.values():
                if product.vendor == vendor:
                    print(product)

    def display_by_product_type(self, product_type):
        if not self.products:
            print("No Stock Available")
        else:
            for product in self.products.values():
                if product.product_type == product_type:
                    print(product)

# SCRAPER CLASS, FOR URL SCRAPER TO FILL PRODUCT CLASS
class Scraper:
    def __init__(self, vendor_url):
        self.vendor_url = vendor_url

    def __str__(self):
        return f"scraper(vendor_url ={self.vendor_url})"
    # TYPICAL USE OF BEAUTIFUL SOUP FOR HTML PARSING
    def fetch_page(self):
        response = requests.get(self.vendor_url)
        self.soup = BeautifulSoup(response.text, "html.parser")

# DEVELOPMENT OF NORMALISATION ENGINE, WHEN PARSING VENDOR HTML, NEW TERMS WILL BE ADDED HERE WHERE RELEVANT, EACH DEF TITLE IS OBVIOUS
class NormalisationEngine:
    def __init__(self, soup):
        self.soup = soup

    def find_product_name(self):
        for class_name in ["product-name", "product-title", "item-name", "product__name", "product_title", "item_name"]:
            result = self.soup.find(class_=class_name)
            if result:
                return result.get_text(strip=True)
        return None

    def find_price(self):
        for class_price in ["product-price", "product-cost", "item-price", "product__price", "product_cost", "item_price"]:
            result = self.soup.find(class_=class_price)
            if result:
                return result.get_text(strip=True)
        return None

    def find_pic_url(self):
        for class_pic_url in ["product-img", "product-pic", "item-img", "product__img", "product_pic", "item_picture"]:
            result = self.soup.find(class_=class_pic_url)
            if result:
                return result.get("src")
        return None

    def find_brand(self):
        for class_brand in ["product-brand", "product-source", "item-brand", "product__brand", "product_source", "item_brand"]:
            result = self.soup.find(class_=class_brand)
            if result:
                return result.get_text(strip=True)
        return None

    def find_product_type(self):
        for class_type in ["dairy", "chilled", "meat", "tinned", "canned", "baked"]:
            result = self.soup.find(class_=class_type)
            if result:
                return result.get_text(strip=True)
        return None

    def find_availability(self):
        for class_availability in ["stock", "availability", "in_stock", "available", "unavailable", "out_of_stock", "discontinued"]:
            result = self.soup.find(class_=class_availability)
            if result:
                return result.get_text(strip=True)
        return None

# DEF FOR NUTRIENT INFO FROM PARSING, KEEPS TRACK PER 100G, EASIER TO USE IN UK DUE TO NUTRIENT LABELLING LAWS
    def find_nutrient_info(self):
        table = None 
        for class_nutrient_info in ["nutrition-info", "Nutrition-Info", "nutrition-table", "Nutrition-Table", "nutrition_info", "Nutrition_Info", "nutrition_table", "Nutrition_Table"]:
            table = self.soup.find(class_=class_nutrient_info)
            if table:
                break 
        if not table:
            return NutritionInfo ("Not Found", "Not Found", "Not Found", "Not Found", "Not Found", "Not Found", "Not Found", "Not Found", "Not Found", "Not Found", "Not Found")
        Energy_label = table.find(string="Energy")
        kcal = Energy_label.find_next("td").get_text(strip=True) if Energy_label else "Not Found"
        Protein_label = table.find(string="Protein")
        Protein = Protein_label.find_next("td").get_text(strip=True) if Protein_label else "Not Found"
        Carbohydrates_label = table.find(string="Carbohydrates")
        Carbohydrates = Carbohydrates_label.find_next("td").get_text(strip=True) if Carbohydrates_label else "Not Found"
        Sugars_label = table.find(string="Sugars")
        Sugars = Sugars_label.find_next("td").get_text(strip=True) if Sugars_label else "Not Found"
        Fat_label = table.find(string="Fat")
        Fat = Fat_label.find_next("td").get_text(strip=True) if Fat_label else "Not Found"
        Fibre_label = table.find(string="Fibre")
        Fibre = Fibre_label.find_next("td").get_text(strip=True) if Fibre_label else "Not Found"
        Salt_label = table.find(string="Salt")
        Salt = Salt_label.find_next("td").get_text(strip=True) if Salt_label else "Not Found"
        Allergens_text = self.soup.find(string=lambda text: text and "Contains" in text)
        Allergens = Allergens_text.split(":")[1].split(",") if Allergens_text else ["Not Found"]
        Vegetarian = bool(self.soup.find(string="Suitable for vegetarians"))
        Vegan = bool(self.soup.find(string="Suitable for vegans"))
        Ingredients_text = self.soup.find(string=lambda text: text and "Ingredients" in text)
        Ingredients = Ingredients_text.split(":")[1].split(",") if Ingredients_text else ["Not Found"]
        return NutritionInfo(kcal, Protein, Carbohydrates, Sugars, Fat, Fibre, Salt, Vegetarian, Vegan, Allergens, Ingredients)
# BOOLEAN USED ABOVE
# SCRAPE MANAGER - NOT OVERLY COMPLICATED
class ScrapeManager:

    def __init__(self, vendor_urls, product_manager):
        self.vendor_urls = vendor_urls
        self.product_manager = product_manager

    def __str__(self):
        return f"Vendor_Urls(Vendor_Urls = {self.vendor_urls}, product_manager = {self.product_manager})"
    
    # ALLOWS FOR THE CACHE REFRESH, USERS SHOULD ONLY EVER INTERACT WITH CACHE, NOT LIVE SCRAPING, SETS CACHE TO RESET EVERY 30 MINUTES
    def refresh_cache(self):
        for vendor, url in self.vendor_urls.items():
            scraper = Scraper(url)
            scraper.fetch_page()
            engine = NormalisationEngine(scraper.soup)
            name = engine.find_product_name()
            price = engine.find_price()
            pic_url = engine.find_pic_url()
            brand = engine.find_brand()
            product_type = engine.find_product_type()
            availability = engine.find_availability()
            nutrient_info = engine.find_nutrient_info()
            self.product_manager.add_product(name, brand, price, availability, product_type, vendor, nutrient_info, pic_url)

# ALLOWS CACHE RESET TO RUN FOREVER WITH A 30 MIN DELAY BETWEEN SCRAPES 
    def run_forever(self):
        while True:
            self.refresh_cache()
            time.sleep(1800)

# REMOVE VENDOR URLS WHEN RUNNING AS FULL PROGRAM FROM UI, CURRENT URL'S HARDCODED HERE, WILL NEED TO BE REMOVED
def main(): 
    product_manager = ProductManager()
    vendor_urls = {
    "Morrisons": "https://www.morrisons.com/products",
    "Tesco": "https://www.tesco.com/groceries"
}
    scrape_manager = ScrapeManager(vendor_urls, product_manager)
    scrape_manager.run_forever()
if __name__ == "__main__":
    main()
