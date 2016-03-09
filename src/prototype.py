from sys import *
import itertools

contries = set(["China"])
products = set(["PyCharm"])
download_words = {"downloads", "download", "downloaded"}

def ask_events_database(ask_word, participent, action, date):
        print("events, ", ask_word, participent, action, date)
        print()
        
def ask_download_database(ask_word, product, contry, date):
        print("downloads, ", ask_word, product, contry, date) 
        print()

def ask_money_database(ask_word, product, base, country):
        print("money, ", ask_word, product, base, country)
        print()         
        
def ask_nation_base(word, retrun_group = None):
        if (retrun_group != None): return "a"
        else: return False
def ask_country_base(word, retrun_group = None):
        if (retrun_group != None): return "a"
        else:
                if (word in contries):
                        return True 
                else: 
                        return False
def ask_product_base(word, retrun_group = None):
        if (word in products):
                return True
        else:
                return False        
        
def events_hendler(words):
        ask_word = "date"
        participent = words[2]
        possible_datas = set()
        action = None
        for word in words:
                if (word.isdigit()):
                        possible_datas.add(word)
        if (words[1] == "is"):
                if (len(words) > 4 and words[3][-3:-1] == "ing"):
                        action = words[3]
        elif (len(words) > 3):
                if (not word.isdigit()): action = words[3]
        if (len(possible_datas) == 0): possible_datas.add(None)                
        for data in possible_datas:
                ask_events_database(ask_word, participent, action, data)
                        
                                                                        
def download_hendler(words):
        ask_word = "how many downloads"
        possible_products = set()
        possible_countries = set()
        possible_dates = set()
        for word in words:
                if (ask_product_base(word) != 0):
                        possible_products.add(word)
        if (len(possible_products) == 0): possible_products.add(None)  
        
        previous_word = None                      
        for word in words:          
                if (previous_word == "in") and (ask_country_base(word) != 0):
                        possible_countries.add(word)
                elif (word in download_words) and (ask_nation_base(previous_word) != 0):
                        possible_countries.add(ask_nation_base(previous_word,"country"));                                                      
                previous_word = word
        if (len(possible_countries) == 0): possible_countries.add(None)
        for word in words:
                if (word.isdigit()):
                        possible_dates.add(word)
        if (len(possible_dates) == 0): possible_dates.add(None)                        
        variants = itertools.product(possible_products, possible_countries, possible_dates)
        for variant in variants:
                ask_download_database(ask_word, variant[0], variant[1], variant[2])                               
                        
        
def money_hendler(words):
        possible_products = set()
        possible_dates = set()
        possible_countries = set()                               

        for word in words:
                if (ask_product_base(word) != 0):
                        possible_products.add(word)
        if (len(possible_products) == 0): possible_products.add(None)

        for word in words:
                if (word.isdigit()):
                        possible_dates.add(word)
        if (len(possible_dates) == 0): possible_dates.add(word)                        

        previous_word = None
        for word in words:
                if (previous_word == "in" and ask_country_base(word)):
                        possible_countries.add(word)
                if (ask_nation_base(previous_word) and word == "customers"):
                        possible_countries.add(ask_nation_base(previous_word, "country"))
                previous_word = word
        if (len(possible_countries) == 0): possible_countries.add(None)

        variants = itertools.product(possible_products, possible_dates, possible_countries);
        if ("customers" in words):
                ask_word = "count of customers"
        else:
                ask_word = "count of sold products"
        for variant in variants:
                ask_money_database(ask_word, variant[0], variant[1], variant[2]);
                                                

def who_function(words):
        print("who, Incorrect question, please try again.")
        print()
def what_function(words):
        print("what, Incorrect question, please try again.")
        print()
def how_function(words):
        if (words[1] != "many"):
                print("Incorrect question, please try again.")
                print()
                return
        if (len(set(words) & download_words) == 0):
                money_hendler(words)
        else: download_hendler(words)
        
def where_function(words):
        print("Incorrect question, please try again.")
def when_function(words):
        events_hendler(words)

words = input().split()
words[-1] = words[-1][0:-1]
print(words)

question_words = {
        "Who": who_function,
        "What": what_function,
        "How": how_function,
        "Where": where_function,
        "When": when_function,        
}

question_words[words[0]](words)
