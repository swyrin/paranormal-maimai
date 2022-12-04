from enum import Enum

__all__ = ["MaimaiUser"]

class MaimaiUserTitleRarity(Enum):
    Normal = 1
    Bronze = 2
    Silver = 3
    Gold = 4
    Rainbow = 5


class MaimaiUser:
    """A maimai user"""
    def __init__(self, username: str, rating: str, title: str, title_rarity: str, stars: str, tour_leader_url: str):
        self.username: str = username
        self.rating: int = int(rating)
        self.title: str = title
        self.title_rarity: MaimaiUserTitleRarity = MaimaiUserTitleRarity[title_rarity]
        self.stars_count: int = int(stars.replace("×", ""))
        self.tour_leader_url: str = tour_leader_url
        
