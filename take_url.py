import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urljoin
import time
import csv
import os


CSV_FILE = "boks_urls.csv"

if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["URL"])

# Завантажити вже зібрані URL, щоб не дублювати
all_urls = set()
with open(CSV_FILE, newline="") as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        all_urls.add(row[0])


# 2. ЗАПУСК БРАУЗЕРА
options = uc.ChromeOptions()
options.add_argument("--start-maximized")
driver = uc.Chrome(options=options)
wait = WebDriverWait(driver, 10)

driver.get("https://books.toscrape.com/")
time.sleep(2)  
# 3. ОТРИМАННЯ ЖАНРІВ
genre_links = []
genres = driver.find_elements(By.CSS_SELECTOR, "ul.nav-list ul li a")

for g in genres:
    href = g.get_attribute("href")
    full_url = urljoin("https://books.toscrape.com/", href)
    genre_links.append(full_url)

print(f"🔎 Знайдено жанрів: {len(genre_links)}")

# 4. ОБХІД ЖАНРІВ І ЗБІР КНИЖОК
for genre_url in genre_links:
    driver.get(genre_url)
    print(f"\n📚 Обробка жанру: {genre_url}")

    while True:
        try:
            wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "product_pod")))
            books = driver.find_elements(By.CSS_SELECTOR, "h3 a")

            new_links = []

            for book in books:
                href = book.get_attribute("href")
                full_url = urljoin(driver.current_url, href)
                if full_url not in all_urls:
                    all_urls.add(full_url)
                    new_links.append(full_url)

            # Зберігаємо в CSV
            if new_links:
                with open(CSV_FILE, "a", newline="") as f:
                    writer = csv.writer(f)
                    for link in new_links:
                        writer.writerow([link])

            print(f"✅ Знайдено {len(new_links)} нових книг на сторінці.")

            # Перевірка наявності кнопки next
            try:
                next_btn = driver.find_element(By.CLASS_NAME, "next")
                next_href = next_btn.find_element(By.TAG_NAME, "a").get_attribute("href")
                next_url = urljoin(driver.current_url, next_href)
                driver.get(next_url)
                time.sleep(2)
            except:
                print("🔚 Жанр завершено (немає наступної сторінки)")
                break

        except Exception as e:
            print(f"❌ Помилка під час обробки сторінки: {e}")
            break
        
driver.quit()
print(f"\n🎉 Готово! Загалом зібрано {len(all_urls)} унікальних книжкових URL.")
