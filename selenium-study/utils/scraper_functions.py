#!/usr/bin/env python3

import traceback as t

from bs4 import BeautifulSoup as bs

def get_data(page_source: str) -> dict:
  temp_meaning = ''
  temp_tags = ''

  try:
    soup = bs(page_source, 'html.parser')

    # Get the topmost result
    topmost_result = soup.find('div', class_='concept_light')

    # Get the tags
    meanings_list_tags = topmost_result.find('div', class_='concept_light-meanings').find_all('div', class_='meaning-tags')
    word_tags = meanings_list_tags[0].text

    temp_tags = word_tags if word_tags else 'none'

    # Get all meanings and concatenate into one string
    meanings_list = topmost_result.find('div', class_='concept_light-meanings').find_all('div', class_='meaning-wrapper')

    for i in range(len(meanings_list_tags)):
      tag_text = meanings_list_tags[i].text
      if(
        tag_text.lower().find('wikipedia') == -1
        and tag_text.lower().find('note') == -1
        and tag_text.lower().find('other') == -1
      ):
        _meaning = meanings_list[i].find('span', class_='meaning-meaning').text
        if _meaning:
          if i == 0:
            temp_meaning =  _meaning
          else:
            temp_meaning = temp_meaning + '; ' + _meaning
    
    return {
      'meaning': temp_meaning if temp_meaning else 'none'
      , 'tags': temp_tags
    }
  
  except Exception as e:
    print(f"\nAn error occured: {e}\n")
    t.print_exc()

    return {
      'meaning': 'none'
      , 'tags': 'none'
    }