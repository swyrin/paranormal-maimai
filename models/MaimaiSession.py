import aiohttp
from bs4 import BeautifulSoup
from typing_extensions import Final, LiteralString

__all__ = ["MaimaiSession"]

class MaimaiSession:
    """Basic maimaiDX client session, I hope it works."""

    def __init__(self, headers=None, *, ssid: str = ""):
        """Create a session for this maimai instance."""
        if not headers:
            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "Connection": "keep-alive",
            }

        self.ssid = ssid
        self.headers: dict = headers
        self.session: aiohttp.ClientSession = aiohttp.ClientSession(
            headers=self.headers
        )
        self.AUTH_URL: Final[
            LiteralString
        ] = "https://lng-tgk-aime-gw.am-all.net/common_auth/login"
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
            url_with_ssid = response.history[1].url.human_repr()
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

        async with self.session.get(self.HOME_URL, params={"ssid": self.ssid}) as response:
            text = await response.text()
            soup = BeautifulSoup(text, "html.parser")
            title = [*soup.find_all("title")][0].text
            return title != "maimai DX NET－Error－" # I know that '-' is an Unicode

    async def logout(self) -> bool:
        """'Log-out' from the session. Returns True if logged out successfully."""
        self.session.headers["Referer"] = "https://maimaidx-eng.com/maimai-mobile/home/userOption/"

        async with self.session.get(f"{self.HOME_URL}/home/userOption/logout/?"):
            pass

        async with self.session.get(self.HOME_URL) as response:
            text = await response.text()
            soup = BeautifulSoup(text, "html.parser")
            title = [*soup.find_all("title")][0].text
            return title == "Login|maimai DX NET"
