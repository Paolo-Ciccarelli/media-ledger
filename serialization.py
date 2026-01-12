import json
from datetime import date
from media import Media, Book, Movie, Anime, Television
from media_library import MediaLibrary
from typing import Optional

def _date_to_str(d: Optional[date]) -> Optional[str]:
    """
    Purpose: converts a datetime.date object to a string for savefile writing.
    """
    if d is None:
        return None
    return d.isoformat()

def _str_to_date(s: Optional[str]) -> Optional[date]:
    """
    Purpose: converts a string to a datetime.date object for savefile loading.
    """
    if not s:
        return None
    return date.fromisoformat(s)

def media_to_dict(m: Media) -> dict:
    basecase = {
        "global_id": m._global_ID,
        "type": type(m).__name__,
        "title": m.title,
        "length": m.length,
        "completion_status": m.completion_status,
        "date_completed": _date_to_str(m.date_completed),
        "release_date": _date_to_str(m.release_date)
    }
    # Handles individual subclasses of Media
    if isinstance(m, Book):
        basecase.update({
            "local_id": m.localID,
            "author": m.author,
            "binding": m.binding,
            "publisher": m.publisher
        })
    elif isinstance(m, Movie):
        basecase.update({
            "local_id": m.localID,
            "director": m.director,
            "watched_in_theatres": m.watched_in_theatres,
            "streaming_platform": m.streaming_platform,
            "distributor": m.distributor 
        })
    elif isinstance(m, Anime):
        basecase.update({
            "local_id": m.localID,
            "episodes_watched": m.episodes_watched,
            "episodes_total": m.episodes_total,
            "num_seasons": m.num_seasons,
            "director": m.director
        })
    elif isinstance(m, Television):
        basecase.update({
            "local_id": m.localID,
            "episodes_watched": m.episodes_watched,
            "episodes_total": m.episodes_total,
            "num_seasons": m.num_seasons,
            "platform": m.platform,
            "showrunner": m.showrunner
        })    
    return basecase

def dict_to_media(d: dict) -> Media:
    """
    Purpose: converts a dictionary back to a Media object for savefile loading.
    """
    media_type = d.get("type")

    # Common fields for all Media types
    common_kwargs = {
        "title": d.get("title"),
        "completion_status": d.get("completion_status", False),
        "date_completed": _str_to_date(d.get("date_completed")),
        "release_date": _str_to_date(d.get("release_date"))
    }

    if media_type == "Book":
        return Book(
            **common_kwargs,
            pages=d.get("length", 0) or 1,
            author=d.get("author", "Unknown Author"),
            binding=d.get("binding", "Unknown"),
            publisher=d.get("publisher")
        )
    elif media_type == "Movie":
        return Movie(
            **common_kwargs,
            length=d.get("length", 0) or 1,
            director=d.get("director"),
            watched_in_theatres=d.get("watched_in_theatres", False),
            streaming_platform=d.get("streaming_platform"),
            distributor=d.get("distributor")
        )
    elif media_type == "Anime":
        return Anime(
            **common_kwargs,
            episodes_watched=d.get("episodes_watched", 0),
            episodes_total=d.get("episodes_total", 1),
            num_seasons=d.get("num_seasons", 1),
            director=d.get("director")
        )
    elif media_type == "Television":
        return Television(
            **common_kwargs,
            episodes_watched=d.get("episodes_watched", 0),
            episodes_total=d.get("episodes_total", 1),
            num_seasons=d.get("num_seasons", 1),
            platform=d.get("platform"),
            showrunner=d.get("showrunner")
        )
    else:
        raise ValueError(f"Unknown media type: {media_type}")
    
def save_library(library: MediaLibrary, filename: str) -> None:
    data = {
        "media": [media_to_dict(m) for m in library._all_media],
        "counters": {
            "global_id": Media.globalID_counter,
            "book_id": Book.localID_counter,
            "movie_id": Movie.localID_counter,
            "anime_id": Anime.localID_counter,
            "television_id": Television.localID_counter
        }
    }
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

def load_library(filename: str) -> MediaLibrary:
    with open(filename, 'r') as f:
        data = json.load(f)

    # Restore counters first
    Media.globalID_counter = data["counters"]["global_id"]
    Book.localID_counter = data["counters"]["book_id"]
    Movie.localID_counter = data["counters"]["movie_id"]
    Anime.localID_counter = data["counters"]["anime_id"]
    Television.localID_counter = data["counters"]["television_id"]

    # Rebuild library
    library = MediaLibrary()
    for media_dict in data["media"]:
        media = dict_to_media(media_dict)
        library.insert_media(media)
    return library
