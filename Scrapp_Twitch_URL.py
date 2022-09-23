import json 
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time 

# test list 
streamers = ['summit1g', 'shroud', 'timthetatman', 'xqcow', 'sodapoppin', 'lirik', 'drdisrespectlive', 'ninja', 'sykkuno', 'disguisedtoasths']

def extract_text (text, start, end) :
    return text.split(start)[1].split(end)[0]

def extract_website (url) : 
    if 'www' in url : 
        return extract_text(url , 'www.' , '/')
    else : 
        return extract_text(url , '//' , '/')

def driver () :
    driver = webdriver.Chrome(ChromeDriverManager().install())
    return driver

def get_url (streamer) :
    url = 'https://www.twitch.tv/{}/about'.format(streamer)
    driver.get(url)
    time.sleep(5)
    return driver

def get_links (driver) :
    l = driver.find_elements_by_tag_name("a")
    links= []
    for link in l : 
        links.append(str(link.get_attribute("href")))
    return links


# function to parse the get generic links
def parse_links (links) :
    parsed_links = []
    for link in links : 
        link_parsed = extract_website(link) 
        if 'twitch' in link_parsed.lower(): 
            pass 
        elif link_parsed in parsed_links :
            pass 
        else:
            parsed_links.append(link_parsed)
    return parsed_links

def main (streamers) :
    links = {}
    for streamer in streamers : 
        driver = get_url(streamer)
        links = get_links(driver)
        parse_links(links)
    return links

if __name__ == '__main__' :
    driver = driver()
    dictionnary_link = main(streamers)
    # export the dictionnary to a json file
    with open('links.json', 'w') as f:
        json.dump(dictionnary_link, f)
        