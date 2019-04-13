from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import os, sys
import requests
from bs4 import BeautifulSoup as bs

def login():
  chrome.get('https://hi10anime.com/wp-login.php')
  chrome.find_element_by_id('user_login').send_keys(username)
  chrome.find_element_by_id('user_pass').send_keys(password)
  chrome.find_element_by_name("wp-submit").click()
  sleep(2)

def format_link(link):
  return link[link.find('=http')+1::]

def Quality(quality):
  try:
    result = chrome.find_element_by_xpath('//*[contains(@id, "{}pane")]'.format(quality))
    chrome.find_element_by_xpath('//*[contains(@id, "{}")]'.format(quality)).click()
    return True, result
  except:
    return False, chrome

def search_category(anime_name):
  chrome.get('https://hi10anime.com/projects/all-projects')
  table = chrome.find_element_by_class_name('categories')
  for item in table.find_elements_by_xpath('.//a'):
    if anime_name.lower() in item.text.lower():
      print('Category Found : {}'.format(item.get_attribute('href')))
      return item.get_attribute('href')
  return False

def search(anime_page, anime_links = [], anime_names = []):
  soup = bs(requests.get(anime_page).content, 'lxml')
  for anime in soup.find_all('h1', {'class':'entry-title'}):
    anime_links.append(anime.find('a')['href'])
    anime_names.append(anime.get_text())
    print('Anime: {}'.format(anime.get_text()))
    print('Link : {}'.format(anime.find('a')['href']))
  try:
    next_page = soup.find('a', {'class':'next page-numbers'})['href']
    chrome.get(next_page)
    return search(next_page, anime_links, anime_names)
  except:
    return anime_links, anime_names

def close_tabs():
  while True:
    try:
      chrome.switch_to.window(chrome.window_handles[1])
      chrome.close()
      chrome.switch_to.window(chrome.window_handles[0])
    except IndexError:
      return

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
      except:
        pass
  except:
    for quality in ['1080','720','480']:
      result, quality = Quality(quality)
      if result:
        break
    sleep(1)
    try:
      for table in quality.find_elements_by_class_name('showLinksTable'):
        for episodes in table.find_elements_by_xpath('.//tr'):
          try:
            a = episodes.find_element_by_xpath('.//a')
            a.click()
            if len(chrome.window_handles) > 50:
              close_tabs()
            episode_links.append(format_link(a.get_attribute('data-href')))
          except:
            pass
    except:
      pass
    try:
      for table in quality.find_elements_by_class_name('episodeTable'):
        for episodes in table.find_elements_by_xpath('.//tr'):
          try:
            a = episodes.find_element_by_xpath('.//a')
            a.click()
            if len(chrome.window_handles) > 50:
              close_tabs()
            episode_links.append(format_link(a.get_attribute('data-href')))
          except:
            pass
    except:
      pass

  return episode_links

def format_name(anime_name):
  anime_name = anime_name[:anime_name.find('[')]
  anime_name = [i for i in anime_name]
  for k,char in enumerate(anime_name):
    c = ord(char)
    if c == 32 or 48 <= c <= 57 or 65 <= c <= 90 or 97 <= c <= 122:
      continue
    else:
      anime_name[k] = ''
  return ''.join(anime_name)

def idm(episode_links, anime_name):
  os.chdir('C:\Program Files (x86)\Internet Download Manager')
  print('{} : '.format(anime_name))
  for k,link in enumerate(episode_links):
    os.popen('IDMan.exe -a -d {}'.format(link))
    print('Episode {} Added to Queue'.format(k+1))
    sleep(1)

def make_file(episode_links, anime_name):
  print('Making File {}'.format(format_name(anime_name)))
  with open('{} Download Links.txt'.format(format_name(anime_name)), 'w') as f:
    for link in episode_links:
      f.write(link)
      f.write('\n')

scriptname, username, password, *anime_name, result = tuple(sys.argv)

if scriptname == os.path.basename(__file__):
  with webdriver.Chrome() as chrome:
    login()
    try:
      anime_name = int(anime_name[0])
      anime_links = ['https://hi10anime.com/archives/{}'.format(anime_name)]
      chrome.get(anime_links[0])
      soup = bs(chrome.page_source, 'lxml')
      anime_names = [soup.find('h1', {'class':'entry-title'}).get_text()]
    except ValueError:
      anime_name = ' '.join(anime_name)
      anime_page = search_category(anime_name)
      if not anime_page:
        print('Anime Not Found')
        exit()
      else:
        chrome.get(anime_page)
        anime_links, anime_names = search(anime_page)

    episode_links = []

    for anime_link in anime_links:
      episode_links.append(run(anime_link))
    for ep_link, anime_name in zip(episode_links, anime_names):
      if len(ep_link) == 0:
        continue
      if result == 'idm':
        idm(ep_link, anime_name)
      elif result == 'txt':
        make_file(ep_link, anime_name)