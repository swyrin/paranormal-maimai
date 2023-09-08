# paranormal-maimai

This is just a playground for me to mess with SEGA's "maimaiDX International Version" website. If you are a *somewhat-devoted* maimai player, I think you know [where the title comes from](https://www.youtube.com/watch?v=L_M599WSXlc).

As of 9 September 2023, this tool will empower [nameless*](https://github.com/nameless-on-discord/nameless) with its features.

# Basic Usage

```python
from models import MaimaiSession

async def example():
    session = MaimaiSession()
    await session.get_ssid_from_credentials(username="your-sega-id-username", password="your-sega-id-password")
    await session.login()
    await session.logout()
```
