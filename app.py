import requests
import json
from bs4 import BeautifulSoup

print("Now, I will ask you for some credentials about your SEGA ID")
SID = input("Your SEGA ID: ")
is_sega_id = False
j = {}

try:
    with open("accounts.json", mode="r", encoding="utf8") as f:
        j = json.load(f)
        _ = j[SID]
except (KeyError, FileNotFoundError, json.JSONDecodeError):
    is_sega_id = True

HEADER = {
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
    "Connection": "keep-alive",
}

MOI_INDEX_URL = "https://maimaidx-eng.com/maimai-mobile"
MOI_LOGIN_URL = "https://lng-tgk-aime-gw.am-all.net/common_auth/login"


with requests.Session() as session:
    session.headers.update(HEADER)

    if is_sega_id:
        PWD = input("Your SEGA ID password: ")

        BODY = {
            "retention": 1,
            "sid": SID,
            "password": PWD,
        }

        r = session.get(
            MOI_LOGIN_URL,
            params={
                "site_id": "maimaidxex",
                "redirect_url": "https://maimaidx-eng.com/maimai-mobile/",
                "back_url": "https://maimai.sega.com/",
            },
        )

        SESSION_ID = ";".join([f"{k}={v}" for k, v in r.cookies.items()])
        session.headers["Cookie"] = SESSION_ID

        session.post(f"{MOI_LOGIN_URL}/sid", data=BODY)

    else:
        session.headers["Cookie"] = j[SID]

    r = session.get(
        MOI_LOGIN_URL,
        params={
            "site_id": "maimaidxex",
            "redirect_url": "https://maimaidx-eng.com/maimai-mobile/",
            "back_url": "https://maimai.sega.com/",
        },
    )

    session.get(f"{MOI_INDEX_URL}/home")

    # Parsing and stuffs
    soup = BeautifulSoup(r.text, "html.parser")
    name = [*soup.find_all("div", {"class": "name_block f_l f_16"})][0].text
    rating = [*soup.find_all("div", {"class": "rating_block"})][0].text

    print("Your name is", name)
    print("Your rating is", rating)

print(
    "If you return to web version to log out and see a 200004 error, well, that is a known issue, but your account is still safe, I guess?"
)

print("And if you did that, you have to get your new session cookie, sorry :<")

with open("accounts.json", mode="w", encoding="utf8") as f:
    json.dump(j, f)
