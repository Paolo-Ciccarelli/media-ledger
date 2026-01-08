from typing import Optional, List, Dict, Type, Union
from datetime import date
from media import Media, Book, Movie, Anime, Television

class MediaLibrary:
    def __init__(self):
        self._all_media: List[Media] = []         # Ordered List for tabular view
        self._media_by_ID: Dict[int, Media] = {}  # Quick lookup by globalID
        self._media_by_type: Dict[Type, List[Media]] = {
            Book: [],
            Movie: [],
            Anime: [],
            Television: [],
        }    

    def insert_media(self, media: Media) -> None:
        self._all_media.append(media)
        self._media_by_ID[media._global_ID] = media

        # For type-specific list insertion
        media_type = type(media)
        if media_type in self._media_by_type:
            self._media_by_type[media_type].append(media)
    
    def update_episodes_watched(self, media: Media, new_count: int) -> None:
        """
        Purpose:
            Updates the number of episodes watched for an episodic media item.
            In other words, the method applies only to media objects that are instances of Episodic.
        Parameters:
            media: the episodic media object whose watched episode count is to be updated.
            new_count: the new number of episodes watched, must be a positive integer.
        """
        if not isinstance(media, Anime):
            return
        # Ensure this exact object is one tracked under its concrete type
        if media not in self._media_by_type.get(type(media), []):
            return

        if 0 <= new_count <= media.episodes_total:
            media.episodes_watched = new_count   

    def get_count(self) -> int:
        """
        Returns: 
            the total number of media items belonging to the ledger.
        """
        return len(self._all_media)
    
    def get_count_byType(self, type: Type) -> int:
        """
        Parameters:
            type: the type of media in question (ie: Anime, Book, Movie, etc)
        Returns:
            the total number of media items of the given type
        """
        return len(self._media_by_type.get(type, []))

