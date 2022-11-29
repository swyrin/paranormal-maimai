import requests
from bs4 import BeautifulSoup

print("I will ask you for the cookie for your account, don't worry, this will not be stored")
print("Here is how to get the cookie:")
print("0. Press Ctrl+Shift+I in advance")
print("1. Go to https://maimaidx-eng.com/maimai-mobile/home/ and login WITH SEGA ID if needed")
print("\tIf you already logged in, logout and login again, we need some data not from already logged in sessions")
print("2. Press Ctrl + Shift + I, go to the one with '/sid', move down to the 'Request Headers' section")
print("3. You should see one with a long wall of text, copy it for the next prompt")
print("Remarks: You should do it every time you run this script")
COOKIE = input("So, can I ask for the cookie: ")

print("Now, I will ask you for some credentials about your SEGA ID")
SID = input("What is your SEGA ID? ")
PWD = input("What is your SEGA ID password? ")

print("If you return to web version and see a 200004 error, well, that is a known issue, but your account is still safe, I guess?")

HEADER = {
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
    "Referer": "https://lng-tgk-aime-gw.am-all.net/common_auth/login?site_id=maimaidxex&redirect_url=https://maimaidx-eng.com/maimai-mobile/&back_url=https://maimai.sega.com/",
    "Connection": "keep-alive",
    "Cookie": COOKIE,
}

MOI_INDEX_URL = "https://maimaidx-eng.com/maimai-mobile"
MOI_LOGIN_URL = "https://lng-tgk-aime-gw.am-all.net/common_auth/login/sid/"

BODY = {
    "retention": 0,
    "sid": SID,
    "password": PWD,
}

with requests.Session() as session:
    r = session.post(MOI_LOGIN_URL, headers=HEADER, data=BODY, verify=False)
    soup = BeautifulSoup(r.text, "html.parser")
    name = [*soup.find_all("div", {"class": "name_block f_l f_16"})][0].text
    rating = [*soup.find_all("div", {"class": "rating_block"})][0].text
    print("Your name is", name, "and your rating is", rating)
