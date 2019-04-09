from selenium import webdriver
from time import sleep
import os, sys
import requests
from bs4 import BeautifulSoup as bs

def login():
  chrome.get('https://hi10anime.com/wp-login.php')
  emailfield = chrome.find_element_by_id('user_login')
  emailfield.send_keys(username)
  passfield = chrome.find_element_by_id('user_pass')
  passfield.send_keys(password)
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

def search(anime_name):
  anime_links, anime_names = [], []
  search_url = 'https://hi10anime.com/?s=' + anime_name
  soup = bs(requests.get(search_url).content, 'lxml')
  try:
    soup =  soup.find_all('h1', {'class':'entry-title'})
  except AttributeError:
    print('Anime Not Found')
    return False
  for anime_page in soup:
    try:
      anime_links.append(anime_page.find('a')['href'])
      anime_names.append(anime_page.get_text())
    except AttributeError:
      pass
  if len(anime_links) > 0:
    return anime_links, anime_names
  print('Anime Not Found')
  return False, False

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
          if len(chrome.window_handles) > 15:
            close_tabs()
          episode_links.append(format_link(a.get_attribute('data-href')))
        except:
          pass

  return episode_links

def idm(episode_links, anime_name):
  os.chdir('C:\Program Files (x86)\Internet Download Manager')
  print('{} : '.format(anime_name))
  for k,link in enumerate(episode_links):
    os.popen('IDMan.exe -a -d {}'.format(link))
    print('Episode {} Added to Queue'.format(k+1))
    sleep(1)

def make_file(episode_links, anime_name):
  with open('{} Download Links.txt'.format(anime_name.title()), 'w') as f:
    for link in episode_links:
      f.write(link)
      f.write('\n')

scriptname, username, password, *anime_name, result = tuple(sys.argv)

if scriptname == os.path.basename(__file__):

  try:
    anime_name = int(anime_name[0])
    anime_links = ['https://hi10anime.com/archives/{}'.format(anime_name)]
    soup = bs(requests.get(anime_links[0]).content, 'lxml')
    anime_names = [soup.find('h1', {'class':'entry-title'}).get_text()]
  except ValueError:
    anime_name = ' '.join(anime_name)
    anime_links, anime_names = search(anime_name)

  episode_links = []
  if anime_links:
    with webdriver.Chrome() as chrome:
      login()
      for anime_link in anime_links:
        episode_links.append(run(anime_link))
    print(len(episode_links), len(anime_names))
    for ep_link, anime_name in zip(episode_links, anime_names):
      if result == 'idm':
        idm(ep_link, anime_name)
      elif result == 'txt':
        make_file(ep_link, anime_name)