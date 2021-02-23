from bs4 import BeautifulSoup
from discord import Embed

def get_og_embed(text: str) -> Embed:
    soup = BeautifulSoup(text, "lxml")

    parts = {}

    for item in soup.find_all("meta"):
        if a := item.get("property"):
            if a.startswith("og:"):
                itype = a[3:]
                icontent = item.get("content")

                parts[itype] = icontent

    kwargs = {}
    for part in {"title", "description", "url"}:
        if part in parts:
            kwargs[part] = parts.pop(part)

    embed = Embed(**kwargs)

    for part, value in parts.items():
        if part == "image":
            embed.set_image(url=value)

    return embed
