import asyncio

from session import MaimaiSession

username = input("What is your SEGA ID username: ")
password = input("What is your SEGA ID password: ")


async def main():
    maimai = MaimaiSession()
    await maimai.get_ssid_from_credentials(username=username, password=password)
    await maimai.login()
    print(await maimai.resolve_user_data())
    await maimai.logout()
    await maimai.close_session()


asyncio.run(main())
