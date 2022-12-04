import asyncio

from models import MaimaiSession


async def main():
	maimai = MaimaiSession()
	await maimai.get_ssid_from_credentials(username="", password="")
	await maimai.login()
	await maimai.logout()


asyncio.run(main())