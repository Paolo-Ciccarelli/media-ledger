from media import Movie, Television
from media_library import MediaLibrary
from datetime import date

media_library = MediaLibrary()

media_object1 = Television(
    title = "Stranger Things", 
    episodes_total= 42, 
    episodes_watched= 42, 
    num_seasons = 5, 
    release_date=date(2016, 7, 15), 
    date_completed=date(2025, 11, 25),
    platform="Netflix",
    completion_status=True)

media_object2 = Movie(
    title= "Wake Up Dead Man", 
    length=144, 
    director= "Rian Johnson",
    streaming_platform="Netflix", 
    completion_status=True)

media_library.insert_media(media_object1)
media_library.insert_media(media_object2)
media_library.display_contents()

