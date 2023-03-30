from src.ratestack.domain.models import Ports, Prices, Regions
from src.ratestack.adapters.repository import SqlAlchemyRepository
import pytest
from datetime import date
from tests.utils import dump_data


def insert_sample_record_in_prices(session):
    session.execute(
        "INSERT INTO prices (orig_code, dest_code, date, price) VALUES "
        '("ABC", "DFG", "2022-05-06", 20), ("ABC", "DFG", "2023-04-05", 45)'
    )


def test_repository_can_save_regions(session):
    region = Regions("SLUG_NAME", "Region Name", None)
    repo = SqlAlchemyRepository(session)
    repo.add(region)
    session.commit()

    rows = list(session.execute('SELECT slug, name, parent_slug FROM regions'))
    assert rows == [("SLUG_NAME", "Region Name", None)]


def test_repository_can_save_ports(session):
    region = Regions("SLUG_NAME", "Region Name", None)
    repo = SqlAlchemyRepository(session)
    repo.add(region)
    session.commit()

    port = Ports("AME", "Port Name", "SLUG_NAME")
    repo = SqlAlchemyRepository(session)
    repo.add(port)
    session.commit()

    rows = list(session.execute('SELECT code, name, parent_slug FROM ports'))
    assert rows == [("AME", "Port Name", "SLUG_NAME")]


def test_repository_can_save_prices(session):
    region = Regions("SLUG_NAME", "Region Name", None)
    repo = SqlAlchemyRepository(session)
    repo.add(region)
    session.commit()

    port = Ports("AME", "Port Name", "SLUG_NAME")
    repo.add(port)
    session.commit()

    price = Prices("AME", "AME", date.today(), 50)
    repo.add(price)
    session.commit()

    rows = list(session.execute(
        'SELECT orig_code, dest_code, date, price FROM prices'))
    assert rows == [("AME", "AME", str(date.today()), 50)]


@dump_data
def test_repository_get_price_by_date(session):
    data = {"date_from": "2022-05-05",
            "date_to": "2022-05-06"}
    repo = SqlAlchemyRepository(session)
    assert repo.get_price(
        **data) == [(10.0, '2022-05-05'), (35.0, '2022-05-06')]


@dump_data
def test_repository_get_price_by_date_from(session):
    data = {"date_from": "2022-05-06"}
    repo = SqlAlchemyRepository(session)
    assert repo.get_price(**data) == [(35.0, '2022-05-06')]


@dump_data
def test_repository_get_price_by_date_to(session):
    data = {"date_to": "2022-04-08"}
    repo = SqlAlchemyRepository(session)
    assert repo.get_price(**data) == [(30.0, '2022-04-05'),
                                      (40.0, '2022-04-06'), (20.0, '2022-04-08')]


@dump_data
def test_repository_get_price_by_origin_and_destination(session):
    data = {"origin": "BB", "destination": "CC"}
    repo = SqlAlchemyRepository(session)
    assert repo.get_price(
        **data) == [(30.0, '2022-04-05'), (20.0, '2022-04-08')]


@dump_data
def test_repository_get_price_by_origin(session):
    data = {"origin": "BB"}
    repo = SqlAlchemyRepository(session)
    assert repo.get_price(**data) == [(30.0, '2022-04-05'),
                                      (40.0, '2022-04-06'), (20.0, '2022-04-08')]


@dump_data
def test_repository_get_price_by_destination(session):
    data = {"destination": "CC"}
    repo = SqlAlchemyRepository(session)
    assert repo.get_price(
        **data) == [(30.0, '2022-04-05'), (20.0, '2022-04-08')]


@dump_data
def test_repository_get_price_by_destination_region_slug(session):
    data = {"destination": "second_level"}  # codes are "DD, QQ, MM"
    repo = SqlAlchemyRepository(session)
    result = repo.get_price(**data)
    assert result == [(30.0, '2022-05-06')]


@dump_data
def test_repository_get_price_by_no_params(session):
    repo = SqlAlchemyRepository(session)
    result = repo.get_price()
    assert len(result) == 5
    stored_dates = {"2022-05-05", "2022-05-06", "2022-04-05",
                    "2022-04-06", "2022-04-08"}
    for prices in result:
        assert prices[1] in stored_dates


@dump_data
def test_repository_get_price_by_complex_query(session):
    data = {"date_from": "2022-04-05", "date_to": "2022-04-08",
            "origin": "root", "destination": "AA"}  # codes are "AA, BB, CC"
    repo = SqlAlchemyRepository(session)
    assert repo.get_price(**data) == [(40.0, '2022-04-06')]
