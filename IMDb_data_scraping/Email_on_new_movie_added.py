#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import the necessary required libraries.
import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


# In[2]:


# Gets the movie names on IMDb top 50 list by popularity and returns the list.
def get_movies():
    imdb_url = "https://www.imdb.com/search/title/?groups=top_100&ref_=adv_prv"
    headers = {"Accept-Language": "en-US, en;q=0.5"}
    results = requests.get(imdb_url, headers=headers)
    movie_soup = BeautifulSoup(results.text, "html.parser")
    
    movie_name = []
    movie_div = movie_soup.find_all('div', class_='lister-item mode-advanced')

    for container in movie_div:
        name = container.h3.a.text
        movie_name.append(name)
        
    return movie_name


# In[3]:


# Will send an email with new movie title. Update with your email and paddword.
def send_email(movie_title):
    email_address = "mayank.tripathi8893@gmail.com"
    password = "your_password"
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(email_address, password)

    subject = "New movie added to list"
    body = "The movie {} has been added to your list.".format(movie_title)

    message = "Subject: {}\n\n{}".format(subject, body)

    server.sendmail(email_address, email_address, message)


# In[17]:


# gets the original list of movies to compare.
orig_movies = get_movies()
orig_movies[:5]


# In[18]:


# Checks every 10 seconds indefinitely. Update the frequency to once a day 86400 seconds.
# Let the program run in the background.

import time

while True:
    time.sleep(10)
    new_movies = get_movies()
    new_movies[:5]

    orig_movies.sort()
    new_movies.sort()
    if new_movies == orig_movies:
        print("no new movies added since last time.")
    else:
        for movie in new_movies:
            if movie not in orig_movies:
                send_email(movie)
    orig_movies = new_movies


# In[ ]:




