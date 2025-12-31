# generate_dashboard.py
import requests
import json
import os
from datetime import datetime

# Use a real TMDB API key for reliability (get one free at https://www.themoviedb.org/settings/api)
TMDB_API_KEY = os.getenv("TMDB_API_KEY", "390b35e605f9fc06397f2270f22d8bee")  # Fallback to demo key

def fetch_public_domain_movies():
    movies = []
    # Fetch older movies (likely public domain)
    url = "https://api.themoviedb.org/3/discover/movie"
    params = {
        "api_key": TMDB_API_KEY,
        "primary_release_date.lte": "1965-12-31",
        "sort_by": "popularity.desc",
        "vote_count.gte": 20,
        "page": 1
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()
        for movie in data.get("results", [])[:12]:  # Top 12
            movies.append({
                "title": movie["title"],
                "year": movie["release_date"][:4] if movie["release_date"] else "????",
                "poster": f"https://image.tmdb.org/t/p/w300{movie['poster_path']}" if movie.get("poster_path") else "https://via.placeholder.com/300x450?text=No+Poster"
            })
    except Exception as e:
        print(f"Error: {e}")
        # Fallback movies if API fails
        movies = [
            {"title": "Metropolis", "year": "1927", "poster": "https://image.tmdb.org/t/p/w300/ggL1kKXc31Z7tUuqx8P3Fb0Xq3N.jpg"},
            {"title": "Nosferatu", "year": "1922", "poster": "https://image.tmdb.org/t/p/w300/lZWLKPsFwZuO5Qq1XqWbB4V6LjJ.jpg"}
        ]
    return movies

def generate_html(movies):
    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>My Free Movie Dashboard</title>
  <style>
    :root {{ --bg: #141414; --text: #fff; --card: #181818; --red: #e50914; }}
    body {{ background: var(--bg); color: var(--text); font-family: Arial, sans-serif; padding: 20px; }}
    h1 {{ text-align: center; margin-bottom: 20px; color: var(--red); }}
    .date {{ text-align: center; color: #aaa; margin-bottom: 20px; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 20px; }}
    .card {{ background: var(--card); border-radius: 8px; overflow: hidden; }}
    .poster {{ width: 100%; aspect-ratio: 2/3; object-fit: cover; }}
    .info {{ padding: 10px; }}
    .title {{ font-size: 0.95rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
    .year {{ font-size: 0.85rem; color: #bbb; }}
    .play {{ width: 100%; padding: 8px; background: var(--red); color: white; border: none; border-radius: 4px; cursor: pointer; margin-top: 8px; }}
  </style>
</head>
<body>
  <h1>🎬 My Free Legal Movies</h1>
  <div class="date">Updated: {datetime.now().strftime('%B %d, %Y')}</div>
  <div class="grid">
"""
    for movie in movies:
        encoded_title = movie['title'].replace("'", "\\'")
        html += f"""
    <div class="card">
      <img class="poster" src="{movie['poster']}" onerror="this.src='https://via.placeholder.com/300x450?text=No+Poster'">
      <div class="info">
        <div class="title">{movie['title']}</div>
        <div class="year">{movie['year']}</div>
        <button class="play" onclick="play('{encoded_title}')">▶ Play</button>
      </div>
    </div>
"""
    html += """
  </div>
  <script>
    function play(title) {
      const q = encodeURIComponent(title + ' full movie public domain');
      window.open('https://www.youtube.com/results?search_query=' + q, '_blank');
      window.open('https://archive.org/search?query=' + encodeURIComponent(title), '_blank');
    }
  </script>
</body>
</html>
"""
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("✅ index.html generated!")

if __name__ == "__main__":
    movies = fetch_public_domain_movies()
    generate_html(movies)
