from main import SteamParser

import aiohttp
import pytest


@pytest.mark.parametrize("num_pages", [5, 10, 15, 20])
@pytest.mark.asyncio
async def test_def_state(num_pages):
    data = await SteamParser().parse(num_pages=num_pages)

    for el in data:
        assert len(el) == 14
        assert len(el["developer"]) > 0
        assert len(el["developer"]) == len(el["developer_link"])

        if el["publisher"] is not None:
            assert len(el["publisher"]) > 0
            assert len(el["publisher"]) == len(el["publisher_link"])


@pytest.mark.parametrize("num_pages", [1, 3, 5, 10])
@pytest.mark.asyncio
async def test_hide_free_to_play_games(num_pages):
    data = await SteamParser().parse(num_pages=num_pages, hide_free_to_play=True)

    for el in data:
        assert el["final_price"] > 0





