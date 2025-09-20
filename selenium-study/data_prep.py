# Import helper functions
from .utils import cleaning_functions as cf

# Import necessary modules
import tabula as tb
import pandas as pd
import traceback as t
import time

from pathlib import Path

""" Data preparation: Preparing the data for the webscraping"""

# File path constants
OUTPUT_FOLDER = Path('selenium-study/data/res')
SOURCE_FOLDER = Path('selenium-study/data')

# Load the raw data from the source file
word_list_file_path = SOURCE_FOLDER / 'nihongo_no_mori.pdf'

# Pages: 12 ~ 21 (名詞2文字　412個)
raw_word_list_df = tb.read_pdf(word_list_file_path, pages='12-21', stream=True, pandas_options={'header': None})

# Clean the extracted data
total_result_len = len(raw_word_list_df)
result_df = pd.DataFrame(columns=['word', 'reading']) # the resulting df

for range in range(total_result_len):
  try:
    if range == 0:
      # Perform initial cleaning on the first result by removing unnecessary columns and rows
      initial_df = cf.clean_first_result(raw_word_list_df[range], 2)

      # Clean the resulting df by removing the square prefixes of the kanjis and
      # transforming the result into one df together with the kanji readings
      cleaned_df = cf.clean_mid_result(initial_df)

      # Add the cleaned df to the result df
      result_df = pd.concat([result_df, cleaned_df], ignore_index=True)

    elif range == total_result_len-1:
    # if range == 1 or range == total_result_len-1:
      continue
    else:
      cleaned_df = cf.clean_mid_result(raw_word_list_df[range])

      # Add the cleaned df to the result df
      result_df = pd.concat([result_df, cleaned_df], ignore_index=True)
  except Exception as e:
    print("\nAn error occured: {e}\n")
    t.print_exc()

# Save the resulting df
file_sheet_name_suffix = time.strftime('%y%m%d_%H%M%S', time.localtime())
file_name = 'extracted' + file_sheet_name_suffix + '.xlsx'

result_df.to_excel(
  OUTPUT_FOLDER / file_name
  , index=False
  , sheet_name= 'res_' + file_sheet_name_suffix
)