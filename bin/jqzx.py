# -*- coding=utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def print_log(mesgs):
    for mesg in mesgs:
        print(u"* [] {} {}".format(mesg[0],mesg[1]))
def get_cover(driver):
    print('cover')
    posts  = driver.find_elements_by_class_name("post__cover")
    return [ (ele.get_attribute('alt'),ele.get_attribute('href')) for ele in posts]


def get_latest(driver):
    print('latest_articles')
    articles  = driver.find_elements_by_class_name("article-item__right")

    def extract(article):
         ahref = article.find_element_by_tag_name('a')
         summary = ahref.text + article.find_element_by_tag_name('p').text 
         return (summary,ahref.get_attribute('href'))
          
    return map(extract,articles)
def get_hot_articles(driver):
    print('hot_articles')
    
    articles  = driver.find_elements_by_class_name("hot-item__title")
    def extract(article):
         summary = article.text
         return (summary,article.get_attribute('href'))
    return map(extract,articles)



def main():
    driver = webdriver.Firefox()
    driver.get("https://www.jiqizhixin.com/")

    print_log(get_cover(driver))
    print_log(get_latest(driver))
    print_log(get_hot_articles(driver))
    driver.close()

if __name__ == "__main__":
   main()
