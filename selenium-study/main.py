import pandas as pd
import time as t
import tabula as tb

from webdriver_manager.firefox import GeckoDriverManager

from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

from bs4 import BeautifulSoup as bs

# This line automatically downloads the correct geckodriver and sets the path
driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))

# Load the data
file_path = 'data/vocab_list.xlsx'
vocab_list_df = pd.read_excel(file_path, sheet_name='N2_2文字_名詞')
vocab_list_df = pd.read_excel(file_path, sheet_name='test')

print(vocab_list_df.head())
print(vocab_list_df.word[0])

# Use the driver to open Firefox
driver.get("https://jisho.org/")

search_bar = driver.find_element(By.ID, "keyword")

word_to_search = vocab_list_df.word[0]
search_bar.send_keys(word_to_search)
search_bar.send_keys(Keys.ENTER)

t.sleep(3)

soup = bs(driver.page_source, 'html.parser')

# meanings_div = soup.find_all('div', class_='meanings-wrapper')
topmost_result = soup.find('div', class_='concept_light')

meanings_list_tags = topmost_result.find('div', class_='concept_light-meanings').find_all('div', class_='meaning-tags')
meanings_list = topmost_result.find('div', class_='concept_light-meanings').find_all('div', class_='meaning-wrapper')

temp_meaning = ''
for i in range(len(meanings_list_tags)):
  item = meanings_list_tags[i]
  if(item.text != 'Wikipedia definition' or item.text != 'Notes'):
    temp_meaning = ';'.join([temp_meaning, meanings_list[i].find('span', class_='meaning-meaning').text])

  print(item.text)

for word in vocab_list_df.word:
  search_bar = driver.find_element(By.ID, "keyword")
  search_bar.send_keys(word)
  search_bar.send_keys(Keys.ENTER)


  


"""
search_bar = driver.find_element(By.ID, "keyword")

word_to_search = "検索"  # Or your word from the pandas DataFrame
search_bar.send_keys(word_to_search)
search_bar.send_keys(Keys.ENTER)

try:
    # Find the main container for the first result
    first_result = driver.find_element(By.CSS_SELECTOR, 'div.concept_light')

    # Find the furigana within that container
    furigana_element = first_result.find_element(By.CSS_SELECTOR, 'span.furigana')
    furigana = furigana_element.text
    print(f"Furigana: {furigana}")
except NoSuchElementException:
    print("Furigana not found.")

try:
    meaning_element = first_result.find_element(By.CSS_SELECTOR, 'span.meaning-meaning')
    meaning = meaning_element.text
    print(f"Meaning: {meaning}")
except NoSuchElementException:
    print("Meaning not found.")

try:
    # Find all elements with the 'part_of_speech' class within the first result
    tags_elements = first_result.find_elements(By.CSS_SELECTOR, 'div.meaning-tags')
    #tags = [tag.text for tag in tags_elements]
    tags = tags_elements[0].text
    
    print(f"Tags: {', '.join(tags)}")
except NoSuchElementException:
    print("Tags not found.")
"""