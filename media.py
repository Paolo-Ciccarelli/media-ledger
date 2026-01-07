from datetime import date
from typing import Optional

class Media:
    globalID_counter = 0
    
    def __init__(
        self, 
        title: str, 
        length: int, 
        date_completed: Optional[date]=None, 
        release_date: Optional[date]=None
    ):
        Media.globalID_counter += 1
        self._global_ID = Media.globalID_counter
        
        self.title = title
        self.length = length
        self.release_date = release_date
        self.date_completed = date_completed

class Books(Media):
    localID_counter = 0
    
    def __init__(
        self, 
        title: str, 
        pages: int, #New Alias
        author: str, #New
        binding: str, #New
        date_completed: Optional[date]=None,
        release_date: Optional[date]=None,
        publisher: Optional[str]=None #New
    ):
        super().__init__(title=title, length=pages, date_completed=date_completed, release_date=release_date)
        Books.localID_counter += 1
        self.localID = Books.localID_counter
        
        self.author = author
        self.binding = binding
        self.publisher = publisher

    @property
    def pages(self) -> int:
        return self.length
    
    @pages.setter
    def pages(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("pages must have an integer value")
        if value <= 0:
            raise ValueError("pages must have a positive value")
        self.length = value

class Movie(Media):
    localID_counter = 0
    
    def __init__(
        self, 
        title: str, 
        length: int, 
        date_completed: Optional[date]=None, 
        director: Optional[str]=None, #New
        release_date: Optional[date]=None,
        watched_in_theatres = False, #New
        streaming_platform: Optional[str]=None, #New
        distributor: Optional[str]=None #New
    ):
        super().__init__(title=title, length=length, date_completed=date_completed, release_date=release_date)
        Movie.localID_counter += 1
        self.localID = Movie.localID_counter

        self.director = director
        self.watched_in_theatres = watched_in_theatres
        self.streaming_platform = streaming_platform
        self.distributor = distributor

class Anime(Media):
    localID_counter = 0

    def __init__(
        self, 
        title: str, 
        episodes_total: int, #New Alias 
        episodes_watched: int, #New
        date_completed: Optional[date]=None,
        director: Optional[str]=None, #New
        release_date: Optional[date]=None
    ):
        super().__init__(title=title, length=episodes_total, date_completed=date_completed, release_date=release_date)
        Anime.localID_counter += 1
        self.localID = Anime.localID_counter
        
        self.director = director
        self.episodes_watched = episodes_watched

    @property
    def episodes_total(self) -> int:
        return self.length
    
    @episodes_total.setter
    def episodes_total(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("episodes_total must have an integer value")
        if value <= 0:
            raise ValueError("episodes_total must have a positive value")
        self.length = value



