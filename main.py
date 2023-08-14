from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from collections import Counter
import math
import time 


### Getting Page Data ###
def scraping_for_titles(url):
    

    driver = webdriver.Chrome(ChromeDriverManager().install())
    page = driver.get(url)

    html = driver.execute_script("return document.body.innerHTML")
    soup = BeautifulSoup(html, "html.parser")
    #print(soup)
    
    ### Film Num ###
    raw_num_films = soup.find('h1', attrs={'class': 'section-heading'}).get_text()[:-6]
    num_of_films = int(''.join(i for i in raw_num_films if i.isdigit()))

    #print(num_of_films)

    films_per_page = 28
    page_count = math.ceil(num_of_films / films_per_page)
    #print(page_count)

    ### Titles on Page ###

    titles = []
    if page_count == 1:

        for film_name in soup.find_all('span', attrs={'class':'frame-title'}):
            titles.append(film_name.get_text())
            #print(titles)
            return titles
    
    if page_count > 1:
        for i in range(1, page_count + 1):
            new_url = url + '/page/' + str(i)
            driver.get(new_url)
            time.sleep(3)
            html = driver.execute_script("return document.body.innerHTML")
            soup = BeautifulSoup(html, "html.parser")
            for film_name in soup.find_all('span', attrs={'class':'frame-title'}):
                titles.append(film_name.get_text())
        #print(titles)
        return titles
    else:
        #print(titles)
        return titles

all_watchlists = []

### Replacing friends' usernames in URL ###
# replace URL name with each friend's username in turn.

def retrieve_friends(friends):
    for name in friends: 
        friend_url = "https://letterboxd.com/" + name + "/watchlist/"
        time.sleep(5)
        all_watchlists.append((scraping_for_titles(friend_url)))

    print(all_watchlists)
    return all_watchlists

title_freq = dict()

# Add each movie in each playlist to a dictionary. For each repeat occurence, increment by 1. 
# Initialize new movies with value of 1.
def top_shared(all_watchlists):
    for watchlist in all_watchlists:
        for title in watchlist:
            if title not in title_freq: 
                title_freq[title] = 1
            else: 
                title_freq[title] += 1

    # Sort dictionary, return top 5 in an array.
    # How to resolve ties? 
    sorted_title_freq = dict(sorted(title_freq.items(), key=lambda x:x[1], reverse = True)[:5])
    # print(sorted_title_freq)
    title_array = []
    for i in sorted_title_freq.keys():
        title_array.append(i)
    return title_array
   

def main():
    # Change according to friends' Letterboxd usernames.
    friends = ["bravefish", "DiCee", "stayjohnson"]
    combined_watchlists = retrieve_friends(friends)
    should_watch = top_shared(combined_watchlists)
    print("You and your friends()" + str(friends[1:]) + ", should watch " + str(should_watch[0]) + ", " + str(should_watch[1]) + ", " + str(should_watch[2]) + ", " + str(should_watch[3]) + ", " + str(should_watch[4]) + ", based on your watchlists' similarities.")

# Testing top_shared()
def test_all_wl():
    watchlists=[["When Marnie Was There", "The Batman", "The Prestige", "The Trial of the Chicago Seven", "Jackie", "The Green Knight", "Home Alone", "Little Women", "Birds of Prey", "Interstellar","The Green Knight"],
                ["When Marnie Was There", "Rent", "Tick Tick Boom", "The Batman", "Jackie", "Manchester by the Sea", "The Green Knight", "Little Women", "Lady Bird"],
                ["Psycho", "The Birds", "Vertigo", "Spirited Away", "When Marnie Was There", "Illinois", "Interstellar", "The Batman", "Manchester by the Sea", "Superman", " The Green Knight"]]
    combined_watchlist = top_shared(watchlists)
    top_shared(combined_watchlist)
    
    
if __name__ == "__main__":
    main()






