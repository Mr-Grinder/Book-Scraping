import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import string


with open("boks_urls.csv", "r") as f:
    reader = csv.reader(f)
    next(reader)
    books_urls = [row[0] for row in reader]

options = uc.ChromeOptions()
options.add_argument("--start-maximized")  
driver = uc.Chrome(options=options)
wait = WebDriverWait(driver, 15)

results_meta = []

for book in books_urls[:3]:
    driver.get(book)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
    time.sleep(2)

    try:
            book_name = driver.find_element(By.CSS_SELECTOR, "div.product_main > h1").text
    except:
            book_name = ""
    try:
            book_price = driver.find_element(By.CLASS_NAME, "price_color").text
    except:
            book_price = ""
    try:
            book_availability = driver.find_element(By.CSS_SELECTOR, "p.instock.availability").text
    except:
            book_availability = ""
    try:
            book_rating = driver.find_element(By.CSS_SELECTOR, "p.star-rating")
            classes = book_rating.get_attribute("class").split()
            book_rating = classes[-1]
    except:
            book_rating = ""
    try:
            upc = driver.find_element(By.TAG_NAME, "td").text
    except:
            upc = ""        
            
    results_meta.append({
             "book_name": book_name,
             "book_price": book_price, 
             "book_availability": book_availability.strip(),
             "book_rating": book_rating,
             "book_upc": upc    
         })   
    print("Зібрані книги:", book_name)

results_des = []

for book in books_urls[:3]:
    driver.get(book)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
    time.sleep(2)
    
    try:
            book_name = driver.find_element(By.CSS_SELECTOR, "div.product_main > h1").text
    except:
            book_name = ""
    try:
            book_description = driver.find_element(By.CSS_SELECTOR, "div#product_description ~ p").text
    except:
            book_description = ""        
            
    results_des.append({
            "book_description": book_description
    })        
print("Зібрані дані:", book_name)
      
driver.quit()       
  
if results_meta:
    with open("books.csv", "w", newline="", encoding="utf-8") as csvfile:
     filednames = ["book_name", "book_price", "book_availability", "book_rating", "book_upc" ]
     writer = csv.DictWriter(csvfile, fieldnames=filednames)
     writer.writeheader()
     writer.writerows(results_meta)
    print("Дані збережено!!!")
else:
    print("Нічого не зібрано")
if results_des:
    with open("books_description.csv", "w", newline="", encoding="utf-8") as csvfile:
     filednames = ["book_name", "book_description" ]
     writer = csv.DictWriter(csvfile, fieldnames=filednames)
     writer.writeheader()
     writer.writerows(results_des)
    print("Дані збережено!!!")
else:
    print("Нічого не зібрано")                                
