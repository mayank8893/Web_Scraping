#!/usr/bin/env python
# coding: utf-8

# In[2]:


# Import the necessary required libraries.
import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


# In[3]:


# Get the data from the website using Beautifulsoup.
imdb_url = "https://www.imdb.com/search/title/?groups=top_100&ref_=adv_prv"
headers = {"Accept-Language": "en-US, en;q=0.5"}
results = requests.get(imdb_url, headers=headers)
movie_soup = BeautifulSoup(results.text, "html.parser")


# In[4]:


# Creating empty lists to be filled in by the web content.
movie_name = []
movie_years = []
movie_runtime = []
imdb_ratings = []
metascores = []
number_votes = []
us_gross = []

# Create a movie_div object to find all div objects in movie_soup.
movie_div = movie_soup.find_all('div', class_='lister-item mode-advanced')

# Loop through each object in the movie_div.
for container in movie_div:
        name = container.h3.a.text
        movie_name.append(name)

        year = container.h3.find('span', class_='lister-item-year').text
        movie_years.append(year)

        runtime = container.p.find('span', class_='runtime').text if container.p.find('span', class_='runtime').text else '-'
        movie_runtime.append(runtime)

        imdb = float(container.strong.text)
        imdb_ratings.append(imdb)

        m_score = container.find('span', class_='metascore').text if container.find('span', class_='metascore') else '-'
        metascores.append(m_score)

        nv = container.find_all('span', attrs={'name': 'nv'})

        vote = nv[0].text
        number_votes.append(vote)

        grosses = nv[1].text if len(nv) > 1 else '-'
        us_gross.append(grosses)


# In[7]:


# Putting all the data in a dataframe.       
movies = pd.DataFrame({
'movie_name': movie_name,
'movie_year': movie_years,
'movie_runtime': movie_runtime,
'imdb_ratings': imdb_ratings,
'metascore': metascores,
'number_votes': number_votes,
'us_gross_millions': us_gross,
})

# Use Pandas str.extract to remove all String characters, and save the value as type int 
# for cleaning up the data with Pandas.
movies['movie_year'] = movies['movie_year'].str.extract('(\d+)').astype(int)
movies['movie_runtime'] = movies['movie_runtime'].str.extract('(\d+)').astype(int)
movies['metascore'] = movies['metascore'].astype(int)
movies['number_votes'] = movies['number_votes'].str.replace(',', '').astype(int)
movies['us_gross_millions'] = movies['us_gross_millions'].map(lambda x: x.lstrip('$').rstrip('M'))
movies['us_gross_millions'] = pd.to_numeric(movies['us_gross_millions'], errors='coerce')

movies[:5]


# In[6]:


# Export our movie results to a pretty little .csv file.
movies.to_csv('top_50_movies_by_popularity.csv')


# In[28]:





# In[ ]:




