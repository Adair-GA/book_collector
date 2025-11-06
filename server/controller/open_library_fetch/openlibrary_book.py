import dataclasses

@dataclasses.dataclass
class OpenlibraryBook:
    key: str
    title: str
    editions: list[str]
    languages: list[str]
    author_names: list[str]
    author_keys: list[str]

    def cover_url(self) -> str:
        return f"https://covers.openlibrary.org/b/olid/{self.key}-L.jpg"
