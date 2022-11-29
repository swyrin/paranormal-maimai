import requests
from bs4 import BeautifulSoup


print("Now, I will ask you for some credentials about your SEGA ID")
SID = input("What is your SEGA ID? ")
PWD = input("What is your SEGA ID password? ")

print(
    "If you return to web version to log out and see a 200004 error, well, that is a known issue, but your account is still safe, I guess?"
)

HEADER = {
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
    "Referer": "https://lng-tgk-aime-gw.am-all.net/common_auth/login?site_id=maimaidxex&redirect_url=https://maimaidx-eng.com/maimai-mobile/&back_url=https://maimai.sega.com/",
    "Connection": "keep-alive",
}

MOI_INDEX_URL = "https://maimaidx-eng.com/maimai-mobile"
MOI_LOGIN_URL = "https://lng-tgk-aime-gw.am-all.net/common_auth/login"

BODY = {
    "retention": 0,
    "sid": SID,
    "password": PWD,
}

with requests.Session() as session:
    r = session.get(
        MOI_LOGIN_URL,
        params={
            "site_id": "maimaidxex",
            "redirect_url": "https://maimaidx-eng.com/maimai-mobile/aimeList",
            "back_url": "https://maimai.sega.com/",
        },
    )
    HEADER["Cookie"] = ";".join([f"{k}={v}" for k, v in r.cookies.items()])

    r = session.post(f"{MOI_LOGIN_URL}/sid", headers=HEADER, data=BODY)

    session.get(MOI_INDEX_URL)
    soup = BeautifulSoup(r.text, "html.parser")
    name = [*soup.find_all("div", {"class": "name_block f_l f_16"})][0].text
    rating = [*soup.find_all("div", {"class": "rating_block"})][0].text

    print("Your name is", name)
    print("Your rating is", rating)

    # Logout
    session.get(f"{MOI_INDEX_URL}/home/userOption/")
    session.headers["Referer"] = f"{MOI_INDEX_URL}/home/userOption/"
    session.get(f"{MOI_INDEX_URL}/home/userOption/logout/?")
