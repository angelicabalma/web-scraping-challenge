import pandas as pd
from bs4 import BeautifulSoup
from splinter import Browser
import datetime as dt


def scrape_all():

    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver", headless=True)
    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store in dictionary.
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "hemispheres": hemispheres(browser),
        "weather": twitter_weather(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):

    url = 'https://mars.nasa.gov/news/'
    # In[51]:
    data = {}
    # In[52]:
    
    # In[61]:
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=True)
    # In[54]:
    browser.visit('https://mars.nasa.gov/news/')
    # In[55]:
    html= browser.html
    # In[56]:
    soup = BeautifulSoup(html, 'html.parser')
    # In[57]:
    news_element_slide = soup.select_one('li.slide')
    news_element_slide
    # In[58]:
    news_text = news_element_slide.find('div', 'content_title').get_text()
    news_text
    # In[60]:
    data['news_text']=news_text
    data #mars.data
    news_p = news_element_slide.find('div', 'article_teaser_body').get_text()
    news_p
    return news_text, news_p 


def featured_image(browser):

    url= 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    # In[48]:
    browser.visit('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars')
    # In[49]:
    full_image_element= browser.find_by_id('full_image')

    full_image_element.click()

    browser.is_element_present_by_text('more info',wait_time=1)
    more_info_element=browser.find_link_by_partial_text('more info')
    more_info_element.click()

    html= browser.html 

    soup=BeautifulSoup(html, 'html.parser')

    relative_img = soup.select_one('figure.lede a img').get('src')
    relative_img

    image_url = f"https://www.jpl.nasa.gov{relative_img}"
    image_url
    return image_url




# In[22]:

def twitter_weather(browser):
    #html=browser.html,
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit('https://twitter.com/marswxreport?lang=en')
    html= browser.html
    try:
        soup = BeautifulSoup(html, 'html.parser')
        print(soup)
        tweet = soup.find('div', attrs={"class":"css-901oao"}) #changed class because 'tweet' and 'data-name' has changed to individual class names, could not get tweet
        print(tweet)
        tweet2 = tweet.find('span','css-901oao').get_text()
    except AttributeError as error: 
        print(error)
        tweet2 = ""
    return tweet2

# In[38]:

def mars_facts():
    url = 'https://space-facts.com/mars/'
    df= pd.read_html('https://space-facts.com/mars/')[0]
    df

    df.columns=['Description', 'Value']

    df.to_html()
    return df.to_html()

def hemispheres(browser):
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    hemisphere_img_url =  []
    links = browser.find_by_css('a.product-item h3')
    #hemisphere = {}
        # We have to find the elements on each loop to avoid a stale element exception
        #browser.find_by_css("")[i].click()
        # Next, we find the Sample image anchor tag and extract the href
        # Get Hemisphere title
        # Append hemisphere object to list
        # Finally, we navigate backwards
        #browser.back()
    #hemisphere_image_urls = []
    #links = browser.find_by_css("")

    for i in range(len(links)):
        hemisphere = {}
        browser.find_by_css("a.product-item h3")[i].click()
        sample_element = browser.find_link_by_text("Sample").first
        hemisphere['image_url']=sample_element['href']
        hemisphere['title']=browser.find_by_css('h2.title').text
        hemisphere_img_url.append(hemisphere)
        browser.back()
        
    hemisphere_img_url
    return hemisphere_img_url


