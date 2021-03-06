"""Script to seed database"""

import os
import json
from random import choice, randint
from datetime import datetime

from crud import create_movie, create_user, create_rating
import model
import server

os.system('dropdb ratings')
os.system('createdb ratings')

model.connect_to_db(server.app)
model.db.create_all()

with open('data/movies.json') as f:
    movie_data = json.loads(f.read()) #turns it into a list of dictionaries

movies_in_db = []
for movie_info in movie_data:

    title, overview, poster_path  = (movie_info['title'],
                            movie_info['overview'],
                            movie_info['poster_path'])

    date_str = movie_info['release_date']
    format = "%Y-%m-%d"
    release_date = datetime.strptime(date_str, format)

    #title, overview, release_date, poster_path
    db_movie = create_movie(title, overview, release_date, poster_path)

    movies_in_db.append(db_movie)

#create fake users

for n in range(10):
    email = f'user{n}@gmail.com'
    password = 'test'
    user = create_user(email, password)
    for i in range(10):
        movie_to_rate = choice(movies_in_db)
        score = randint(1,5)
        create_rating(user, movie_to_rate, score)




