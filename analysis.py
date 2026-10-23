from indexing import MovieIndex
from storage import STORAGE_movie_dic

class Analytics:
    def __init__(self, avl_year, avl_genre, avl_title, by_id_dict):
        # Get indices directly
        self.AVL_year = avl_year
        self.AVL_genre = avl_genre
        self.AVL_title = avl_title
        self.by_id = by_id_dict

    def min_year(self):
        """Get the minimum year and sample movies from that year."""
        try:
            # Use entry_set to find min year
            for entry in self.AVL_year.entry_set():
                year = entry.get_key()
                movie_ids = entry.get_value()
                break  # First entry is the minimum

            # Get movies
            movies = []
            for movie_id in movie_ids[:5]:
                if movie_id in self.by_id:
                    movies.append(self.by_id[movie_id])

            return year, movies
        except Exception as e:
            print(f"Error in min_year: {e}")
            return None, []

    def max_year(self):
        """Get the maximum year and sample movies from that year."""
        try:
            # Use entry_set to find max year (last entry)
            last_entry = None
            for entry in self.AVL_year.entry_set():
                last_entry = entry  # Keep updating until last

            if last_entry is None:
                return None, []

            year = last_entry.get_key()
            movie_ids = last_entry.get_value()

            # Get movies
            movies = []
            for movie_id in movie_ids[:5]:
                if movie_id in self.by_id:
                    movies.append(self.by_id[movie_id])

            return year, movies
        except Exception as e:
            print(f"Error in max_year: {e}")
            return None, []

    def average_rating_by_year(self, year):
        movie_ids = self.AVL_year.get(year)
        if not movie_ids:
            return None
        ratings = [self.by_id[mid].get("vote_average", 0) for mid in movie_ids
                   if mid in self.by_id and "vote_average" in self.by_id[mid]]
        if not ratings:
            return None
        return sum(ratings) / len(ratings)

    def median_rating_by_year(self, year):
        movie_ids = self.AVL_year.get(year)
        if not movie_ids:
            return None
        ratings = sorted([self.by_id[mid]["vote_average"] for mid in movie_ids
                          if mid in self.by_id and "vote_average" in self.by_id[mid]])
        if not ratings:
            return None
        n = len(ratings)
        mid = n // 2
        if n % 2 == 0:
            return (ratings[mid - 1] + ratings[mid]) / 2
        return ratings[mid]

    def top_k_movies_by_year(self, year, field="vote_average", k=5):
        movie_ids = self.AVL_year.get(year)
        if not movie_ids:
            return []
        movies = [self.by_id[mid] for mid in movie_ids
                  if mid in self.by_id and field in self.by_id[mid]]
        movies.sort(key=lambda x: x[field], reverse=True)
        return movies[:k]

    def top_k_years(self, k=10, highest=True):
        # Get all entries from AVL tree
        entries = list(self.AVL_year.entry_set())
        counts = [(entry.get_key(), len(entry.get_value())) for entry in entries]
        counts.sort(key=lambda x: x[1], reverse=highest)
        return counts[:k]

    def genre_counts(self):
        entries = list(self.AVL_genre.entry_set())
        return {entry.get_key(): len(entry.get_value()) for entry in entries}

    def most_common_genre(self):
        best_genre, best_count = None, -1
        for entry in self.AVL_genre.entry_set():
            cnt = len(entry.get_value())
            if cnt > best_count:
                best_count, best_genre = cnt, entry.get_key()
        return best_genre, best_count

    def least_common_genre(self):
        worst_genre, worst_count = None, None
        for entry in self.AVL_genre.entry_set():
            cnt = len(entry.get_value())
            if worst_count is None or cnt < worst_count:
                worst_count, worst_genre = cnt, entry.get_key()
        return worst_genre, worst_count

    def average_rating_by_genre(self, genre):
        movie_ids = self.AVL_genre.get(genre)
        if not movie_ids:
            return None
        ratings = [self.by_id[mid].get("vote_average", 0) for mid in movie_ids
                   if mid in self.by_id and "vote_average" in self.by_id[mid]]
        if not ratings:
            return None
        return sum(ratings) / len(ratings)

    def median_rating_by_genre(self, genre):
        movie_ids = self.AVL_genre.get(genre)
        if not movie_ids:
            return None
        ratings = sorted([self.by_id[mid]["vote_average"] for mid in movie_ids
                          if mid in self.by_id and "vote_average" in self.by_id[mid]])
        if not ratings:
            return None
        n = len(ratings)
        mid = n // 2
        if n % 2 == 0:
            return (ratings[mid - 1] + ratings[mid]) / 2
        return ratings[mid]

    def top_k_movies_by_genre(self, genre, field="vote_average", k=5):
        movie_ids = self.AVL_genre.get(genre)
        if not movie_ids:
            return []
        movies = [self.by_id[mid] for mid in movie_ids
                  if mid in self.by_id and field in self.by_id[mid]]
        movies.sort(key=lambda x: x[field], reverse=True)
        return movies[:k]

    def all_titles_sorted(self):
        return [entry.get_key() for entry in self.AVL_title.entry_set()]

    def titles_starting_with(self, prefix):
        movie_ids = self.AVL_title.get_keys_with_prefix(prefix)
        return [self.by_id[mid]["title"] for mid in movie_ids if mid in self.by_id]

    def top_k_titles(self, k=10):
        result = []
        for entry in self.AVL_title.entry_set():
            result.append(entry.get_key())
            if len(result) == k:
                return result
        return result

    def print_summary_report(self):
        """Print a comprehensive analytics report."""
        print("Total movies in database:", len(self.by_id))

        # Count entries in each index
        year_count = sum(1 for _ in self.AVL_year.entry_set())
        genre_count = sum(1 for _ in self.AVL_genre.entry_set())
        title_count = sum(1 for _ in self.AVL_title.entry_set())

        print("Years indexed:", year_count)
        print("Genres indexed:", genre_count)
        print("Titles indexed:", title_count)
        print()

        # Min/Max Year
        min_year, min_movies = self.min_year()
        max_year, max_movies = self.max_year()

        print("Oldest Year:", min_year)
        if min_movies:
            movie_titles = [m.get('title', 'Unknown') for m in min_movies[:3]]
            print("  Sample Movies:", movie_titles)
        print()

        print("Newest Year:", max_year)
        if max_movies:
            movie_titles = [m.get('title', 'Unknown') for m in max_movies[:3]]
            print("  Sample Movies:", movie_titles)
        print()

        # Top-K Years
        print("Top 5 Years by Number of Movies:")
        top_years = self.top_k_years(5)
        for year, count in top_years:
            print(f"  {year}: {count} movies")
        print()

        # Genre stats
        most_genre, most_count = self.most_common_genre()
        least_genre, least_count = self.least_common_genre()

        print(f"Most Common Genre: {most_genre} ({most_count} movies)")
        print(f"Least Common Genre: {least_genre} ({least_count} movies)")
        print()

        # Average Ratings
        print("Average Ratings (sample):")

        sample_years = [2010, 2015, 2020]
        for year in sample_years:
            rating = self.average_rating_by_year(year)
            print(f"  {year}: {rating if rating is not None else 'No data'}")

        sample_genres = ['Drama', 'Action', 'Comedy']
        for genre in sample_genres:
            rating = self.average_rating_by_genre(genre)
            print(f"  {genre}: {rating if rating is not None else 'No data'}")
        print()

        # Top Movies
        print("Sample Top Movies:")
        print("  Top 3 Movies in 2020 by Rating:")
        top_2020 = self.top_k_movies_by_year(2020, k=3)
        if top_2020:
            for i, movie in enumerate(top_2020, 1):
                title = movie.get('title', 'Unknown')
                rating = movie.get('vote_average', 'N/A')
                print(f"    {i}. {title} (Rating: {rating})")
        else:
            print("    No data for 2020")
        print()

        # Titles info
        print("Titles Information:")
        all_titles = self.all_titles_sorted()
        print(f"  Total Titles: {len(all_titles)}")

        # Count titles starting with different letters as shown
        for letter in ['A', 'B', 'C']:
            titles_with_letter = self.titles_starting_with(letter)
            print(f"  Titles starting with '{letter}': {len(titles_with_letter)}")

        print(f"  First 5 Titles Alphabetically:")
        first_titles = self.top_k_titles(5)
        for i, title in enumerate(first_titles, 1):
            print(f"    {i}. {title}")

if __name__ == "__main__":
    index_engine = MovieIndex(dataset=STORAGE_movie_dic)

    by_id_dict = {}
    for movie_id, movie_data in STORAGE_movie_dic.items():
        movie_data_copy = movie_data.copy()
        movie_data_copy['id'] = movie_id
        by_id_dict[movie_id] = movie_data_copy

    analytics = Analytics(
        avl_year=index_engine.AVL_year,
        avl_genre=index_engine.AVL_genre,
        avl_title=index_engine.AVL_title,
        by_id_dict=by_id_dict
    )

    analytics.print_summary_report()