# %%
# Finds the index of the first string in a list of strings that contains a particular substring
def first_substring_index(strings, substring):
    try:
      return next(i for i, string in enumerate(strings) if substring in string) 
    except:
      print("Couldn't find", substring, "in list starting with", strings[0])

# Slices a string up to and including a particular substring
def slice_up_to_substring(string, substring):
  start_index = string.find(substring)
  if start_index == -1:
    print("Couldn't find", substring, "in", string) 
  else:  
    end_index = start_index+len(substring)
    string = string[0:end_index]
    return string

# %%
import requests
from bs4 import BeautifulSoup

def get_wikipedia_url(title, year):
  session = requests.Session()
  search_url  = "https://en.wikipedia.org/w/api.php"
  params = {
      "action": "opensearch",
      "namespace": "0",
      "search": title+" "+year+" film",
      "limit": "5",
      "format": "json"
  }
  try:
    req = session.get(url=search_url, params=params, timeout=1)
  except:
    pass
  data = req.json()
  if len(data[1])==0:
    params["search"] = title
    try:
      req = session.get(url=search_url, params=params, timeout=1)
    except:
      pass
    data = req.json()
    if len(data[1])==0:
      print("Search failed for {} {}.".format(title,year))
      return
  data = req.json()
  article_url = data[3][0]
  return article_url

def wikipedia_first_sentence(title, year):
  article_url = get_wikipedia_url(title, year)
  try:
    req = requests.get(article_url)
  except:
    print("Artical retrieval failed for "+title+", "+year)
    return
  soup = BeautifulSoup(req.content, 'html.parser')
  first_paragraph = soup.find('p', class_ = lambda x: x != "mw-empty-elt")
  text = first_paragraph.contents
  strings = [entry.string for entry in text if entry.string is not None]

  try:   
    index = first_substring_index(strings," film")   
  except:
    print("Couldn't find 'film' in first paragraph for "+title+", "+year+":")
    for entry in range(len(strings)):
      print(entry,strings[entry]) 
    return
  strings[index] = slice_up_to_substring(strings[index],"film")  
  try:
    strings = strings[:index+1]
  except:
    pass
  first_sentence = ""
  for entry in strings:
    first_sentence = first_sentence + entry
  # print(first_sentence)
  return first_sentence

print(wikipedia_first_sentence("Holes","2003"))


