import pandas as pd
import time as t

from .utils import scraper_functions as sf
from pathlib import Path
from webdriver_manager.firefox import GeckoDriverManager

from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# File path constants
OUTPUT_FOLDER = Path('selenium-study/data/res')
SOURCE_FOLDER = Path('selenium-study/data')

# This line automatically downloads the correct geckodriver and sets the path
driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
# driver = webdriver.Firefox()

# Load the data
file_path = SOURCE_FOLDER / 'vocab_list.xlsx'
vocab_list_df = pd.read_excel(file_path, sheet_name='N2_2文字_名詞')
# vocab_list_df = pd.read_excel(file_path, sheet_name='test')

# Use the driver to open Firefox
driver.get("https://jisho.org/")

word_meanings = [] # list to store results' meaning
word_tags = [] # list to store results' tags

search_bar = driver.find_element(By.ID, "keyword")

# Loop over the vocabulary list
for i in range(len(vocab_list_df)):
  # Input word in the search bar and perform search
  word_to_search = vocab_list_df.word[i]
  search_bar.send_keys(word_to_search)
  search_bar.send_keys(Keys.ENTER)
  
  t.sleep(3)
  
  # Get results using helper function
  results = sf.get_data(driver.page_source)

  # Add results to lists
  word_meanings.append(results['meaning'])
  word_tags.append(results['tags'])

  # Clear search bar
  search_bar = driver.find_element(By.ID, "keyword")
  search_bar.clear()

# Add results to the df
vocab_list_df.meaning = word_meanings
vocab_list_df.types = word_tags

# Save results
file_sheet_name_suffix = t.strftime('%y%m%d_%H%M%S', t.localtime())
file_name = 'processed' + file_sheet_name_suffix + '.xlsx'
vocab_list_df.to_excel(
  OUTPUT_FOLDER / file_name
  , index=False
  , sheet_name='results_' + file_sheet_name_suffix
)

# Todo: Close window once the search is done
# Todo: Time elapsed and success notif maybe?
# Todo: Add to helper function on extracting sample sentences as well

# # TEST
# word_to_search = vocab_list_df.word[0]
# search_bar.send_keys(word_to_search)
# search_bar.send_keys(Keys.ENTER)
# t.sleep(3)
# results = sf.get_data(driver.page_source)
# print(results)
# search_bar = driver.find_element(By.ID, "keyword")
# search_bar.clear()

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