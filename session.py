import re
from typing import Optional, Union

import aiohttp
from bs4 import BeautifulSoup, NavigableString, Tag
from models import MaimaiTrack, MaimaiUser
from typing_extensions import Final, LiteralString


__all__ = ["MaimaiSession"]


class MaimaiSession:
    """Basic maimaiDX client session, I hope it works."""

    def __init__(self, *, ssid: str = ""):
        """Create a session for this maimai instance."""
        self.is_logged_in: bool = False
        self.ssid: str = ssid
        self.headers: dict = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Connection": "keep-alive",
        }
        self.session: aiohttp.ClientSession = aiohttp.ClientSession(headers=self.headers)
        self.AUTH_URL: Final[LiteralString] = "https://lng-tgk-aime-gw.am-all.net/common_auth/login"
        self.HOME_URL: Final[LiteralString] = "https://maimaidx-eng.com/maimai-mobile"

    async def get_ssid_from_credentials(self, *, username: str, password: str) -> None:
        """Create a NEW SSID from given SEGA ID username **AND PASSWORD**"""
        async with self.session.get(
            self.AUTH_URL,
            params={
                "site_id": "maimaidxex",
                "redirect_url": self.HOME_URL,
                "back_url": "https://maimai.sega.com/",
            },
        ):
            pass

        async with self.session.post(
            f"{self.AUTH_URL}/sid",
            data={
                "retention": 1,
                "sid": username,
                "password": password,
            },
        ) as response:
            url_with_ssid = response.history[1].url.human_repr()
            self.ssid = self._parse_ssid(url_with_ssid)

    async def get_ssid_from_cookie(self, *, cookie: str) -> None:
        """Create a NEW SSID from given cookie"""
        self.session.headers["Cookie"] = cookie

        async with self.session.get(
            self.AUTH_URL,
            params={
                "site_id": "maimaidxex",
                "redirect_url": self.HOME_URL,
                "back_url": "https://maimai.sega.com/",
            },
        ) as response:
            try:
                url_with_ssid = response.history[1].url.human_repr()
            except IndexError:
                raise ValueError("Invalid account provided")

            self.ssid = self._parse_ssid(url_with_ssid)

    def _parse_ssid(self, url: str) -> str:
        if not url:
            raise ValueError("You passed an invalid URL")

        ssid = url[len(f"{self.HOME_URL}?ssid=") :]

        if ssid:
            return ssid
        else:
            raise ValueError(f"Unable to retrieve SSID from {url}")

    async def login(self) -> bool:
        """'Log-in' from a maimai instance. Returns True if logged in successfully"""
        if not self.ssid:
            raise ValueError(
                "You did not create a valid SSID, you can solve this by calling create_ssid_from_credentials "
                "or create_ssid_from_cookie or pass in the constructor"
            )

        if self.is_logged_in:
            raise RuntimeWarning("You already logged in")

        async with self.session.get(self.HOME_URL, params={"ssid": self.ssid}) as response:
            text = await response.text()
            soup = BeautifulSoup(text, "html.parser")
            title = [*soup.find_all("title")][0].text

            if title != "maimai DX NET－Error－":  # I know that '-' is an Unicode
                self.is_logged_in = True
                return self.is_logged_in
            else:
                return False

    async def logout(self) -> bool:
        """'Log-out' from the session. Returns True if logged out successfully."""
        self.must_be_logged_in()

        self.session.headers["Referer"] = "https://maimaidx-eng.com/maimai-mobile/home/userOption/"
        is_logged_out: bool = False

        async with self.session.get(f"{self.HOME_URL}/home/userOption/logout/?"):
            pass

        async with self.session.get(self.HOME_URL) as response:
            text = await response.text()
            soup = BeautifulSoup(text, "html.parser")
            title = [*soup.find_all("title")][0].text
            is_logged_out = title == "Login|maimai DX NET"

        self.is_logged_in = not is_logged_out
        return is_logged_out

    async def close_session(self) -> None:
        if self.is_logged_in:
            raise RuntimeWarning("You are logged in, you sure that you wanna close the session?")

        await self.session.close()

    def must_be_logged_in(self) -> None:
        if not self.is_logged_in:
            raise RuntimeError("This session is not logged in")

    async def get_html(self, method: str, url: str, **kwargs) -> str:
        """Perform HTTP request and return the url"""
        async with self.session.request(method=method, url=url, **kwargs) as response:
            return await response.text()

    def get_tag(self, html: str, tag_name: str, attr: dict) -> Optional[Union[Tag, NavigableString]]:
        """Find html text with given tag name and attributes"""
        soup = BeautifulSoup(html, "html.parser")
        result = soup.find(tag_name, attr)

        if not result:
            raise RuntimeError("Unable to extract data")

        return result

    async def resolve_user_data(self):
        self.must_be_logged_in()
        user_html = await self.get_html("GET", f"{self.HOME_URL}/home")

        username = self.get_tag(user_html, "div", {"class": "name_block f_l f_16"}).text
        rating: int = int(self.get_tag(user_html, "div", {"class": "rating_block"}).text)
        title = self.get_tag(user_html, "div", {"class": "trophy_inner_block f_13"}).text.replace("\n", "")

        title_rarity = self.get_tag(
            user_html, "div", {"class": re.compile(r"trophy_block trophy_([a-zA-Z]*) p_3 t_c f_0")}
        )["class"][1][
            len("trophy_") :
        ]  # pyright: ignore

        stars = self.get_tag(user_html, "div", {"class": "p_l_10 f_l f_14"}).text

        dan_level_image_url = self.get_tag(user_html, "img", {"class": "h_35 f_l"})["src"][0]  # pyright: ignore

        season_level_image_url = self.get_tag(user_html, "img", {"class": "p_l_10 h_35 f_l"})["src"][
            0
        ]  # pyright: ignore

        avatar_url = self.get_tag(user_html, "img", {"class": "w_112 f_l"})["src"][0]  # pyright: ignore

        tour_leader_image_url = self.get_tag(user_html, "img", {"class": "w_120 m_t_10 f_r"})["src"][
            0
        ]  # pyright: ignore

        user_data_html = await self.get_html("GET", f"{self.HOME_URL}/playerData")
        playcount: int = int(
            self.get_tag(user_data_html, "div", {"class": "m_5 m_t_10 t_r f_12"}).text.replace("play count：", "")
        )

        user_data = MaimaiUser(
            username,
            rating,
            title,
            title_rarity,
            stars,
            tour_leader_image_url,
            dan_level_image_url,
            season_level_image_url,
            avatar_url,
            playcount,
        )

        print(user_data.__dict__)

        return user_data

    def resole_play_data(self):
        self.must_be_logged_in()
        return None
