import streamlit as st
import pickle
import pandas as pd
import requests

st.header('Movie Recommender System')

movies=pd.read_csv('movies.csv')
movie_list=movies['Title'].values
selected_movie=st.selectbox('Type or select a movie from the dropdown',movie_list)

sim=pickle.load(open('sim_mtrix.pkl','rb'))

def recommend(movie_name):
    movie_index=movies[movies['Title']==movie_name].index[0]
    distance=sorted(list(enumerate(sim[movie_index])),reverse=True, key=lambda x:x[1])
    recommend_movies=[]
    posters=[]
    for i in distance[1:6]:
        recommend_movies.append(movies.iloc[i[0]].Title)
        posters.append(fetch_poster(movies.iloc[i[0]].Id))
    return recommend_movies, posters

def fetch_poster(movie_id):
    url=f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=f6af2d00d3718dc7effbc0b047ac367b'
    data=requests.get(url)
    data=data.json()
    poster_path=data['poster_path']
    full_path='https://image.tmdb.org/t/p/w500/'+poster_path
    return full_path

if st.button('Show Recommend'):
    movie_names, posters = recommend(selected_movie)
    for i in range(len(movie_names)):
         st.text(movie_names[i])
         st.image(posters[i])