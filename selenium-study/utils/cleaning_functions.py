#!/usr/bin/env python3

""" Helper functions to clean extracted data"""

import pandas as pd
import traceback as t

def clean_first_result(df: pd.DataFrame, nrows: int) -> pd.DataFrame:
  try:
    # Drop unnecessary columns
    cleaned_df = df.copy()
    cleaned_df = cleaned_df.drop(columns=[1,3,4])

    # Drop unnecessary rows and reset the index
    cleaned_df.drop(range(nrows), axis=0, inplace=True)
    cleaned_df = cleaned_df.reset_index(drop=True)

    # Reset column names for uniformity
    cleaned_df.columns = range(cleaned_df.shape[1])

    # Return the cleaned df
    return cleaned_df
  
  except Exception as e:
    print(f"\nAn error occured: {e}\n")
    t.print_exc()

    return pd.DataFrame()

def clean_mid_result(df: pd.DataFrame) -> pd.DataFrame:
  try:
    cleaned_df = df.copy()

    # Removing the squares from the kanji rows [0, 2]
    kanji_row = pd.concat(
      [
        cleaned_df[0].str[2:]
        , cleaned_df[2].str[2:]
      ]
      , ignore_index=True
    )
    # Merging the corresponding kanji readings [1, 3] into one object
    kanji_reading = pd.concat(
      [
        cleaned_df[1]
        , cleaned_df[3]
      ]
      , ignore_index=True
    )

    # Merging the cleaned kanji and their readings into one dataframe
    final_df = pd.DataFrame(
      {
        'word': kanji_row
        , 'reading': kanji_reading
      }
    )

    # Return the final df
    return final_df
  except Exception as e:
    print(f"\nAn error occured: {e}\n")
    t.print_exc()

    return pd.DataFrame()