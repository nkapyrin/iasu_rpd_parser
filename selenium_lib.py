#encoding:utf-8

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

browser = webdriver.Firefox()
delay = 2 # seconds

def query_book( book_rec ):
  try:
      browser.get("http://elibrary.mai.ru/MegaPro/Web/Search/Simple")
  except:
      browser.get("http://elibrary.mai.ru/MegaPro/Web/Search/Simple")

  browser.find_element_by_css_selector("input[name='cond_words'][type='radio'][value='all']").click
  element = browser.find_element_by_id("simpleCond")
  element.send_keys( book_rec )
  element.submit()

  try:
      myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'rs-data')))
      #
      divs = myElem.find_elements_by_tag_name("div")
      record, content, authors, code, url = '','','','',''
      record = divs[0].text.replace('\n',' ').replace('\r','')
      for div in divs[1:]:
          if u"Шифры:" in div.text: code = div.text.replace('\n',' ').replace('\r',' ').replace(u"Шифры:","").strip()
          if u"Экземпляры:" in div.text: content = div.text.replace('\n',' ').replace('\r','').replace(u"Экземпляры:","").strip()
          if u"Авторы:" in div.text: authors = div.text.replace('\n',' ').replace('\r','').replace(u"Авторы:","").strip()
          if u"Ссылка на ресурс:" in div.text: url = div.text.replace('\n',' ').replace('\r','').replace(u"Ссылка на ресурс:","").strip()

      myType = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'rs-ctr')))
      #print dir(myType.find_elements_by_tag_name("b")[0].text)
      #for i,e in myType.find_elements_by_tag_name("b"): print i, e
      #t = myType.find_elements_by_tag_name("b").text
      t = myType.find_elements_by_tag_name("b")[0].text
      t = t[t.find('. ')+2:]
      
      return ( t, record, authors, content, code, url )
  except TimeoutException:
      #print "Loading took too much time!"
      return None 


if __name__ == "__main__":
  print query_book( u"Фрайден Современные датчики 2006" )
  print query_book( u"Абракадабра" )
