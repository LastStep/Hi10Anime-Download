from selenium import webdriver
from time import sleep
import os, sys
import requests
from bs4 import BeautifulSoup as bs

def login():
  chrome.get('https://hi10anime.com/wp-login.php')
  emailfield = chrome.find_element_by_id('user_login')
  emailfield.send_keys(sys.argv[1])
  passfield = chrome.find_element_by_id('user_pass')
  passfield.send_keys(sys.argv[2])
  chrome.find_element_by_name("wp-submit").click()
  sleep(2)

def format_link(link):
  return link[link.find('=http')+1::]

def Quality(quality):
  try:
    result = chrome.find_element_by_xpath('//*[contains(@id, "{}pane")]'.format(quality))
    chrome.find_element_by_xpath('//*[contains(@id, "{}")]'.format(quality)).click()
    print('{}p Found'.format(quality))
    return True, result
  except:
    return False, chrome

def search(anime_name):
  search_url = 'https://hi10anime.com/?s=' + anime_name
  soup = bs(requests.get(search_url).content, 'lxml')
  try:
    soup =  soup.find('h1', {'class':'entry-title'})
  except AttributeError:
    print('Anime Not Found')
    return False
  try:
    if anime_name.lower() not in soup.find('a').get_text().lower():
      print('Anime Not Found')
      return False
    return soup.find('a')['href']
  except AttributeError:
    print('Anime Not Found')
    return False

def run(anime_link):
  chrome.get(anime_link)
  sleep(3)

  episode_links = []

  try:
    chrome.find_element_by_class_name('button-wrapper').click()
    for episodes in chrome.find_elements_by_class_name('ddl'):
      try:
        a = episodes.find_element_by_xpath('.//a')
        a.click()
        episode_links.append(format_link(a.get_attribute('data-href')))
      except:
        pass

  except:
    for quality in ['1080','720','480']:
      result, quality = Quality(quality)
      if result:
        break
    sleep(2)

    for table in quality.find_elements_by_class_name('showLinksTable'):
      for episodes in table.find_elements_by_xpath('.//tr'):
        try:
          a = episodes.find_element_by_xpath('.//a')
          a.click()
          episode_links.append(format_link(a.get_attribute('data-href')))
        except:
          pass

  return episode_links

def idm(episode_links):
  os.chdir('C:\Program Files (x86)\Internet Download Manager')
  for k,link in enumerate(episode_links):
    os.popen('IDMan.exe -a -d {}'.format(link))
    print('Episode {} Added to Queue'.format(k+1))
    sleep(1)

def make_file(episode_links, anime_name):
  with open('{} Download Links.txt'.format(anime_name.title()), 'w') as f:
    for link in episode_links:
      f.write(link)
      f.write('\n')

if sys.argv[0] == os.path.basename(__file__):
  anime_link = search(sys.argv[3])
  if anime_link:
    with webdriver.Chrome() as chrome:
      login()
      episode_links = run(anime_link)
    if len(sys.argv[0]) == 5 and sys.argv[4] == 'idm':
      idm(episode_links)
    else:
      make_file(episode_links, sys.argv[3])
