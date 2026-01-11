from typing import Optional, List, Dict, Type, Union
from datetime import date
from media import Media, Episodic, Anime, Book, Movie, Television

class MediaLibrary:
    def __init__(self):
        self._all_media: List[Media] = []         # Ordered List for tabular view
        self._media_by_ID: Dict[int, Media] = {}  # Quick lookup by globalID
        self._media_by_type: Dict[Type, List[Media]] = {
            Anime: [],
            Book: [],
            Movie: [],
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
        if not isinstance(media, Episodic): 
            return
        # Ensure this exact object is one tracked under its concrete type
        if media not in self._media_by_type.get(type(media), []):
            return
        # Ensures the new value is positive and does not exceed the total episode count.
        if 0 <= new_count <= media.episodes_total:
            media.episodes_watched = new_count

    def update_total_episodes(self, media: Media, new_count: int) -> None:
        """
        Purpose:
            Updates the total number of episodes belonging to an episodic media item.
            This should occur whenever a new season is officially released, ideally automatically.
            In other words, the method applies only to media objects that are instances of Episodic.
        Parameters:
            media: the episodic media object whose total episode count is to be updated.
            new_count: the new number of total episodes, must be a positive integer.
        """
        if not isinstance(media, Episodic): 
            return
        # Ensure this exact object is one tracked under its concrete type
        if media not in self._media_by_type.get(type(media), []):
            return
        # Ensures the new value is positive and does not exceed the total episode count.
        if 0 <= new_count > media.episodes_total:
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

    def display_contents(self) -> None:
        """
        Displays all media in the library in a formatted table view.
        """
        # Verifies whether the library is empty before proceeding
        if not self._all_media:
            print("ERROR: Library is empty.")
            return

        # Define column widths
        id_width = 5
        type_width = 12
        title_width = 30
        details_width = 60

        # Print header
        header = f"{'ID':<{id_width}} {'Type':<{type_width}} {'Title':<{title_width}} {'Details':<{details_width}}"
        print(header)
        print("-" * (id_width + type_width + title_width + details_width + 3))

        # Print each media item
        for media in self._all_media:
            media_id = str(media._global_ID)
            media_type = type(media).__name__
            title = media.title[:title_width]

            # Generate details based on media type
            if isinstance(media, Book):
                details = f"{media.pages} pages | Author: {media.author}"
            elif isinstance(media, Movie):
                details = f"{media.length} min | Director: {media.director or 'N/A'}"
            elif isinstance(media, Anime):
                details = f"{media.episodes_watched}/{media.episodes_total} eps | {media.num_seasons} seasons"
            elif isinstance(media, Television):
                details = f"{media.episodes_watched}/{media.episodes_total} eps | {media.num_seasons} seasons | Platform: {media.platform or 'N/A'}"
            else:
                details = f"{media.length} units"

            details = details[:details_width]

            row = f"{media_id:<{id_width}} {media_type:<{type_width}} {title:<{title_width}} {details:<{details_width}}"
            print(row)