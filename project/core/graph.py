from storage import STORAGE_movie_dic

class GenreGraph:
    class Vertex:
        def __init__(self, genre):
            self.genre = genre
        
        def __str__(self):
            return str(self.genre)
        
        def __repr__(self):
            return str(self.genre)

    class Edge:
        def __init__(self, u, v, weight=1):
            self.u = u
            self.v = v
            self.weight = weight

    def __init__(self):
        # adjacency map: genre -> {genre: Edge}
        self.adj = {}

    # ----------------- Vertex / Edge Helpers -----------------
    def insert_vertex(self, genre):
        """Create vertex if it doesn’t exist."""
        if genre not in self.adj:
            self.adj[genre] = {}
        return genre

    def insert_edge(self, g1, g2):
        """Insert or increment edge weight between two genres."""
        if g1 not in self.adj:
            self.adj[g1] = {}
        if g2 not in self.adj:
            self.adj[g2] = {}

        if g2 in self.adj[g1]:
            self.adj[g1][g2].weight += 1
        else:
            self.adj[g1][g2] = self.Edge(g1, g2, weight=1)

    # ----------------- Build graph from dataset -----------------
    def build_from_dataset(self, dataset):
        """
        For each movie, connect all genres that co-occur.
        """
        for movie_id, movie_data in dataset.items():
            genres = movie_data.get("genres", [])
            if not genres:
                continue

            # Create vertices
            for g in genres:
                self.insert_vertex(g)

            # Add edges between every pair of genres
            for i in range(len(genres)):
                for j in range(i + 1, len(genres)):
                    g1 = genres[i]
                    g2 = genres[j]
                    self.insert_edge(g1, g2)
                    self.insert_edge(g2, g1)

    # ----------------- Shortest path (BFS) -----------------
    def shortest_path(self, start, goal):
        """
        BFS shortest path between two genres.
        """
        if start not in self.adj or goal not in self.adj:
            return None

        from collections import deque
        queue = deque([start])
        parent = {start: None}

        while queue:
            g = queue.popleft()

            if g == goal:
                # reconstruct path
                path = []
                cur = g
                while cur is not None:
                    path.append(cur)
                    cur = parent[cur]
                path.reverse()
                return path

            for neigh in self.adj[g]:
                if neigh not in parent:
                    parent[neigh] = g
                    queue.append(neigh)

        return None

    # ----------------- Top-K Degrees -----------------
    def top_k_degrees(self, k):
        """
        Return top-k genres by number of connections (degree).
        """
        degree_list = []

        for g in self.adj:
            degree = len(self.adj[g])
            degree_list.append((g, degree))

        degree_list.sort(key=lambda x: x[1], reverse=True)
        return degree_list[:k]

    # ----------------- Algorithm 3: Genre Popularity Score -----------------
    def genre_popularity_score(self, genre):
        """
        Sum popularity of all movies that contain the given genre.
        """

        total = 0
        for movie in STORAGE_movie_dic.values():
            if genre in movie.get("genres", []):
                pop = movie.get("popularity", 0)
                if isinstance(pop, (int, float)):
                    total += pop

        return total
