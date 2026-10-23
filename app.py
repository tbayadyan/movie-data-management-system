import sys
import os

sys.path.append(r"C:\Users\Yoga 7i\Desktop\classes_f2\3. DSA\project\core")

import streamlit as st
from query_engine import QueryEngine
from indexing import MovieIndex
from storage import STORAGE_movie_dic
from graph import GenreGraph

import streamlit as st
from query_engine import QueryEngine
from indexing import MovieIndex
from storage import STORAGE_movie_dic
from graph import GenreGraph

# Initialize the necessary objects
index_engine = MovieIndex(dataset=STORAGE_movie_dic)
query_engine = QueryEngine(movie_dic=STORAGE_movie_dic)

# Create genre graph
genre_graph = GenreGraph()
genre_graph.build_from_dataset(STORAGE_movie_dic)

# Streamlit Sidebar: Search by movie title, year, and genre
st.sidebar.header("Movie Search")
search_option = st.sidebar.radio("Choose Search Type", ("By Title", "By Year", "By Genre"))

if search_option == "By Title":
    movie_title = st.sidebar.text_input("Enter Movie Title")
    if movie_title:
        result = query_engine.search_by_title(movie_title)
        if result:
            st.write(f"**{result['title']}** ({result['release_date']})")
            st.write(f"Rating: {result['vote_average']} | Popularity: {result['popularity']}")
            st.write(f"Overview: {result['overview']}")
        else:
            st.write("No movie found.")

elif search_option == "By Year":
    movie_year = st.sidebar.number_input("Enter Year", min_value=1900, max_value=2025)
    if movie_year:
        result = query_engine.search_by_year(movie_year)
        if result:
            st.write(f"Movies from {movie_year}:")
            for movie in result:
                st.write(f"**{movie['title']}** - Rating: {movie['vote_average']}")
        else:
            st.write("No movies found for this year.")

elif search_option == "By Genre":
    movie_genre = st.sidebar.selectbox("Select Genre", options=["Action", "Comedy", "Drama", "Thriller", "Adventure", "Horror"])
    if movie_genre:
        result = query_engine.search_by_genre(movie_genre)
        if result:
            st.write(f"Movies in {movie_genre} genre:")
            for movie in result:
                st.write(f"**{movie['title']}** - Rating: {movie['vote_average']}")
        else:
            st.write("No movies found for this genre.")

# Genre Graph Analysis: Display top genres or graph
st.sidebar.header("Genre Graph")
graph_option = st.sidebar.radio("Choose Graph Option", ("Top Genres by Degree", "Genre Popularity Score", "Shortest Path Between Genres"))

if graph_option == "Top Genres by Degree":
    k = st.sidebar.number_input("Enter number of top genres to display", min_value=1, max_value=20, value=5)
    top_genres = genre_graph.top_k_degrees(k)
    st.write("Top Genres by Number of Connections (Degree):")
    for genre, degree in top_genres:
        st.write(f"**{genre}**: {degree} connections")

elif graph_option == "Genre Popularity Score":
    genre = st.sidebar.selectbox("Select Genre", options=["Action", "Comedy", "Drama", "Thriller", "Adventure", "Horror"])
    score = genre_graph.genre_popularity_score(genre)
    st.write(f"Total Popularity Score for {genre}: {score}")

elif graph_option == "Shortest Path Between Genres":
    start_genre = st.sidebar.selectbox("Select Starting Genre", options=["Action", "Comedy", "Drama", "Thriller", "Adventure", "Horror"])
    goal_genre = st.sidebar.selectbox("Select Goal Genre", options=["Action", "Comedy", "Drama", "Thriller", "Adventure", "Horror"])
    path = genre_graph.shortest_path(start_genre, goal_genre)
    if path:
        st.write(f"Shortest path from {start_genre} to {goal_genre}: {' -> '.join(path)}")
    else:
        st.write(f"No path found between {start_genre} and {goal_genre}.")

# Optional: Analytics summary
st.header("Movie Analytics Summary")
if st.button("Generate Report"):
    from analysis import Analytics
    analytics = Analytics(query_engine)
    analytics.print_summary_report()

