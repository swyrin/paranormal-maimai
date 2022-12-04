import json
import pytest


from models.MaimaiSession import MaimaiSession

j = {}

with open("tests/account.json", mode="r", encoding="utf8") as f:
    j = json.load(f)


class TestMaiMaiSession:
    @pytest.fixture(autouse=True)
    def fixture(self):
        self.maimai = MaimaiSession()

    def test_default_session(self):
        assert self.maimai.session is not None
        assert self.maimai.headers is not None
        assert self.maimai.ssid is ""

    def test__parse_ssid_good(self):
        assert (
            self.maimai._parse_ssid(
                "https://maimaidx-eng.com/maimai-mobile?ssid=abcdefghijklmnopqrstuxwxyz"
            )
            == "abcdefghijklmnopqrstuxwxyz"
        )
        assert (
            self.maimai._parse_ssid(
                "https://maimaidx-eng.com/maimai-mobile?ssid=0123456789"
            )
            == "0123456789"
        )

    def test__parse_ssid_bad(self):
        with pytest.raises(ValueError):
            self.maimai._parse_ssid("https://maimaidx-eng.com/maimai-mobile/?ssid=")
            self.maimai._parse_ssid("")

    @pytest.mark.asyncio
    async def test_result_from_credentials_good(self):
        await self.maimai.get_ssid_from_credentials(
            username=j["SID"], password=j["PWD"]
        )

    @pytest.mark.asyncio
    async def test_result_from_credentials_bad(self):
        with pytest.raises(IndexError):
            await self.maimai.get_ssid_from_credentials(username="YwY", password="OwO")

    @pytest.mark.xfail(reason="Cookie not always a good choice")
    @pytest.mark.asyncio
    async def test_result_from_cookie_good(self):
        await self.maimai.get_ssid_from_cookie(cookie=j["COOKIE"])

    @pytest.mark.xfail(reason="Cookie not always a good choice")
    @pytest.mark.asyncio
    async def test_result_from_cookie_bad(self):
        with pytest.raises(IndexError):
            await self.maimai.get_ssid_from_cookie(cookie="abc")

    @pytest.mark.xfail(reason="Cookie not always a good choice")
    @pytest.mark.asyncio
    async def test_login_cookie_good(self):
        await self.maimai.get_ssid_from_cookie(cookie=j["COOKIE"])
        await self.maimai.login()

    @pytest.mark.xfail(reason="Cookie not always a good choice")
    @pytest.mark.asyncio
    async def test_login_cookie_bad(self):
        with pytest.raises(IndexError):
            await self.maimai.get_ssid_from_cookie(cookie="abc")
            await self.maimai.login()

    @pytest.mark.asyncio
    async def test_login_credentials_good(self):
        await self.maimai.get_ssid_from_credentials(
            username=j["SID"], password=j["PWD"]
        )
        assert await self.maimai.login() is True

    @pytest.mark.asyncio
    async def test_login_bad_ssid_provide(self):
        self.maimai = MaimaiSession(ssid="123")
        assert await self.maimai.login() is False

    @pytest.mark.asyncio
    async def test_login_bad_no_ssid(self):
        with pytest.raises(ValueError):
            await self.maimai.login()

    @pytest.mark.