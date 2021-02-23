from aiohttp import ClientSession
from asyncio import get_event_loop


class ManagedHTTP:
    def __init__(self):
        self.session = ClientSession()

    async def ensure_session(self):
        if self.session.closed:
            self.session = ClientSession()

    async def request(self, method: str, url: str, *args, **kwargs):
        await self.ensure_session()
        return await self.session.request(method, url, *args, **kwargs)
