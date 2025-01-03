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




