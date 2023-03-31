import uuid
import pytest
import requests
import json
from ratestack import config


@pytest.mark.usefixtures("postgres_db")
@pytest.mark.usefixtures("restart_api")
def test_query_prices():
    url = config.get_api_url()
    r = requests.get(
        f"{url}/rates", json={
            "origin": "CNSGH",
            "destination": "2022-north_europe_main-10",
            "date_from": "2016-01-01",
            "date_to": "2016-01-10"
        }
    )
    assert r.status_code == 200
    assert "rates" in json.loads(r.content)
