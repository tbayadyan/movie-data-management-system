# TMDB Movie Query System

A Python-based movie search, analytics, and genre graph system using the TMDB Movies Dataset (2023). Designed to handle 1.3M+ movie records efficiently with AVL-tree indexing and graph-based genre analysis.

---

## Project Structure

## 1. Storage

**`storage.py`**

**Purpose:** Load the TMDB dataset from CSV or pickle. Maintain `STORAGE_movie_dic` dictionary keyed by unique movie ID.  
**Key Elements:**
  `STORAGE_movie_dic`: `{movie_id: movie_dict}`  
  `storager_obj`: handles unique ID generation.  
**Functions:**
   `getter_next_key_to_insert()`: returns next available ID.
   `setter_next_key_to_insert(new_id)`: updates next available ID.

## 2. Indexing

**`indexing.py`**

**Purpose** Maintain AVL trees for fast search by title, year, and genre.
**Class**: INDEX_searching_engine
AVL_title: AVL tree keyed by movie title → movie ID.
AVL_year: AVL tree keyed by release year → list of movie IDs.
AVL_genre: AVL tree keyed by genre → list of movie IDs.

- **Methods**
`inserting_process(movie, movie_id)`: Insert movie into all AVL trees.
`deleting_process(movie_id)`: Remove movie from AVL trees.
`save_AVL_pickle()`: Persist AVL trees to disk.

## 4. Query Engine

**`query_engine.py`**

**Purpose**: Central interface for querying, inserting, deleting, and modifying movies.
**Class**: QueryEngine
- **Methods** - see in report.pdf


## 5. Genre Graph

**`graph.py`**

**Purpose**: Analyze relationships between movie genres using a graph.
**Internal Classes**:
Vertex: Represents a genre.
Edge: Represents co-occurrence of two genres in movies, with weight.

**Class**: GenreGraph


## 6. Analytics

**`analysis.py`**

**Purpose**: Generate comprehensive analytics reports from the dataset.
**Class**: Analytics
**Methods**: `min_year()` / `max_year()` - earliest/latest movie year and sample movies
`average_rating_by_year(year)` / `median_rating_by_year(year)`
`top_k_movies_by_year(year, field="vote_average", k=5)`
`top_k_years(k=10, highest=True)`
`genre_counts()` - {genre: number of movies}
`most_common_genre()` / `least_common_genre()`
`average_rating_by_genre(genre)` / `median_rating_by_genre(genre)`
`top_k_movies_by_genre(genre, field="vote_average", k=5)`
`all_titles_sorted()`
`titles_starting_with(prefix)`
`top_k_titles(k=10)`
`print_summary_report() → prints a comprehensive report`

## 7. Streamlit App

**`app.py`**

**Purpose**: Interactive front-end for:
Searching movies by Title, Year, Genre
Genre graph analytics (top genres, popularity, shortest paths)
Generating summary reports