from urllib.parse import urlsplit
from selenium import webdriver
from bs4 import BeautifulSoup as bs
from splinter import Browser
from urllib.request import urlopen, urlretrieve
from urllib.parse import urljoin
import os
import urllib
import pandas as pd
import time
def init_browser():

    exec_path = {'executable_path': 'chromedriver'}

    return Browser('chrome', headless=False, **exec_path)


def scrape():

    url1 = 'https://mars.nasa.gov/news/'
    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    url3 = 'https://twitter.com/marswxreport?lang=en'
    url4 = 'http://space-facts.com/mars/'
    url5 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    db_mars_collection ={}
#BEG  NASA
    browser = init_browser()
    browser.visit(url1)

    html = browser.html

    soup = bs(html,"html.parser")

    time.sleep(2)

    news_title = soup.find("div",class_="content_title").text
    news_p = soup.find("div", class_="article_teaser_body").text
    print(f"Title: {news_title}")
    print(f"Paragraph: {news_p}")

#building required dictionary
    db_mars_collection['news_title'] = news_title
    db_mars_collection['news_paragraph'] = news_p
#END  NASA

#BEG JPL
#initialize browser for second web site
    browser.visit(url2)
    time.sleep(2)
   
    browser.find_by_id('full_image').click()
    featured_image_url = browser.find_by_css('.fancybox-image').first['src']
    db_mars_collection['featured_image_url'] = featured_image_url

#END  JPL

#BEG Mars Weather  twitter
    browser.visit(url3)
    time.sleep(2)

    for text in browser.find_by_css('.tweet-text'):
        if text.text.partition(' ')[0] == 'Sol':
            mars_weather = text.text
            break
    db_mars_collection['mars_weather'] = mars_weather
    print(mars_weather)
#EMD Mars Weather  twitter

#BEG  FACTS TABLE 
    browser.visit(url4)
    time.sleep(2)

    df = pd.read_html(url4, attrs={'id': 'tablepress-mars'})[0]
    time.sleep(2)
    df = df.set_index(0).rename(columns={1: "value"})
    del df.index.name
    time.sleep(2)
    mars_facts = df.to_html(justify='left')

    db_mars_collection['mars_facts'] = mars_facts
#END  FACTS TABLE 

## No soup just splinter 
    browser.visit(url5)
    time.sleep(2)

#Find titles with tag h3 and assign     
    title1 = browser.find_by_tag('h3')[0].text
    title2 = browser.find_by_tag('h3')[1].text
    title3 = browser.find_by_tag('h3')[2].text
    title4 = browser.find_by_tag('h3')[3].text
    time.sleep(2)

#Finding the image location   
    browser.find_by_css('.thumb')[0].click()
    time.sleep(2)
    first_img = browser.find_by_text('Sample')['href']
    browser.back()
    time.sleep(2)
    browser.find_by_css('.thumb')[1].click()
    second_img = browser.find_by_text('Sample')['href']
    browser.back()
    time.sleep(2)

    browser.find_by_css('.thumb')[2].click()
    third_img = browser.find_by_text('Sample')['href']
    browser.back()
    time.sleep(2)

    browser.find_by_css('.thumb')[3].click()
    fourth_img = browser.find_by_text('Sample')['href']
    time.sleep(2)

    hemisphere_image_urls = [
        {'title': title1, 'img_url': first_img},
        {'title': title2, 'img_url': second_img},
        {'title': title3, 'img_url': third_img},
        {'title': title4, 'img_url': fourth_img}
    ]
    time.sleep(2)
    db_mars_collection['hemisphere_image_urls'] = hemisphere_image_urls
    time.sleep(2)
    return(db_mars_collection)

