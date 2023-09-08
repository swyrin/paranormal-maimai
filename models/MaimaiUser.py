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

    def __init__(
        self,
        username: str,
        rating: str,
        title: str,
        title_rarity: str,
        stars: str,
        tour_leader_url: str,
        dan_level_url: str,
        season_level_url: str,
        avatar_url: str,
        play_count: int,
    ):
        # /home
        self.username: str = username
        self.rating: int = int(rating)
        self.title: str = title
        self.title_rarity: MaimaiUserTitleRarity = MaimaiUserTitleRarity[title_rarity]
        self.stars_count: int = int(stars.replace("×", ""))
        self.tour_leader_url: str = tour_leader_url
        self.dan_level_url: str = dan_level_url
        self.season_level_url: str = season_level_url
        self.avatar_url: str = avatar_url

        # /playerData
        self.play_count: int = play_count
        self.total_track_count: int = 0  # convenience data
        # Score
        self.count_SSS_plus: int = 0
        self.count_SSS: int = 0
        self.count_SS_plus: int = 0
        self.count_SS: int = 0
        self.count_S_plus: int = 0
        self.count_S: int = 0
        self.count_clear: int = 0
        # AP/FC
        self.count_AP_plus: int = 0
        self.count_AP: int = 0
        self.count_FC_plus: int = 0
        self.count_FC: int = 0
        # FDX/FS
        self.count_FDX_plus: int = 0
        self.count_FDX: int = 0
        self.count_FS_plus: int = 0
        self.count_FS: int = 0
        # DX score(?)
        self.count_DX_5_stars: int = 0
        self.count_DX_4_stars: int = 0
        self.count_DX_3_stars: int = 0
        self.count_DX_2_stars: int = 0
        self.count_DX_1_stars: int = 0
