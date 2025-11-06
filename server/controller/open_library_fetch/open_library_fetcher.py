import httpx

from server.controller.open_library_fetch.exceptions.invalid_openlibrary_response import (
    InvalidOpenLibraryResponse,
)
from server.controller.open_library_fetch.openlibrary_book import OpenlibraryBook


class OpenLibraryFetcher:
    def __init__(self):
        self.client = httpx.AsyncClient()
        self.base_url = "https://openlibrary.org/search.json"

    async def search(self, query: str) -> list[OpenlibraryBook]:
        response = await self.client.get(
            self.base_url,
            params={
                "q": query,
                "fields": "title,edition_key,language,key,author_name,author_key",
            },
        )

        response_json = response.json()

        if "docs" not in response_json:
            raise InvalidOpenLibraryResponse()

        return [
            OpenlibraryBook(
                key=doc["key"].removeprefix("/works/"),
                title=doc["title"],
                languages=doc["language"],
                editions=doc["edition_key"],
                author_keys=doc["author_key"],
                author_names=doc["author_name"],
            )
            for doc in response_json["docs"]
        ]


