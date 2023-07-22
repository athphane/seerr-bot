import aiohttp

from overseerrbot import config


class OverseerrApi:
    def __init__(self):
        self.base_url = config.get('web_api', 'url') + '/api/v1'
        self.api_key = config.get('web_api', 'api_key')

        self.headers = {'X-Api-Key': self.api_key}

    async def _request(self, method, endpoint, data=None):
        url = f"{self.base_url}/{endpoint}"
        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, json=data, headers=self.headers) as response:
                return await response.json()

    async def _get(self, endpoint: str, data=None):
        return await self._request("GET", endpoint, data)

    async def _post(self, endpoint: str, data):
        return await self._request("POST", endpoint, data)

    async def get_status(self):
        return await self._get("status")

    async def get_requests_count(self):
        return await self._get("request/count")

    async def get_requests(self):
        data = {
            "take": 20,
            "filter": "pending",
            "sort": "-added"
        }

        return await self._get("request", data)

    async def get_movie_details(self, movie_id: int):
        return await self._get(f"movie/{movie_id}")

    async def get_tv_details(self, tv_id: int):
        return await self._get(f"tv/{tv_id}")

    async def get_media_details(self, type: str, media_id: int):
        if type == "movie":
            return await self.get_movie_details(media_id)
        elif type == "tv":
            return await self.get_tv_details(media_id)

        return None

    async def approve_request(self, request_id: int):
        return await self._post(f"request/{request_id}/approve", {})

    async def deny_request(self, request_id: int):
        return await self._post(f"request/{request_id}/decline", {})

    @staticmethod
    async def get_poster(poster_url: str):
        tmdb_link = 'https://image.tmdb.org/t/p/w600_and_h900_bestv2'
        poster_url = f"{tmdb_link}{poster_url}"

        async with aiohttp.ClientSession() as session:
            async with session.get(poster_url) as response:
                return await response.read()