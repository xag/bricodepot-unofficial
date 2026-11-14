"""The wood panels Brico Dépôt France lists, as data on furniture-design's kinds (source, clause, material),
each line read as a board of wood-panels. Unofficial: Brico Dépôt neither wrote nor endorsed it.

What the shop lists comes from its public product sitemap (range.json, read by tools/read_range.py from the
sitemap files as fetched): every product whose title or address states a board, its line, thickness and sheet
size. Each is a clause under sources/bricodepot-sitemap. wood_panels.shops reads the titles and makes the materials:
one per line and thickness, `bricodepot-<line>-<thickness>`, its payload `shop` saying what is sold and which
board its values are.
Its FAQ says 'Nos dépôts ne proposent pas ce service.': it does not cut.

    from furniture_design.knowledge import knowledge as general, merge
    from wood_panels import knowledge as wood_panels
    from bricodepot_unofficial import knowledge as bricodepot
    tree.root.children = merge(general(), wood_panels(), bricodepot()) + [pieces]
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

from quern.tree import Node
from wood_panels import shops

HERE = Path(__file__).parent
SHOP = "Brico Dépôt"
PREFIX = "bricodepot"
SOURCE = "bricodepot-sitemap"


@lru_cache(maxsize=1)
def rows() -> list[dict]:
    return json.loads((HERE / "range.json").read_text(encoding="utf-8"))



def knowledge() -> list[Node]:
    """The branches to merge beside furniture-design's and wood-panels's: the sources, the materials."""
    out = shops.knowledge(PREFIX, SHOP, SOURCE, "Brico Dépôt France, product sitemap (https://www.bricodepot.fr/sitemaps/sitemap.xml)",
                          "https://www.bricodepot.fr/sitemaps/sitemap.xml", "2026-11-14", rows())
    return out
