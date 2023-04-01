import pytest

from ratestack.domain.models import Ports, Prices, Regions
from tests.utils import dump_ports, dump_prices, dump_regions


@dump_regions
def test_regions_mapper_can_load_regions(session):
    expected = [
        Regions("root", "root region"),
        Regions("first_level", "First Level", "root"),
        Regions("second_level", "Second Level", "first_level"),
    ]
    assert session.query(Regions).all() == expected


@dump_ports
def test_ports_mapper_can_load_ports(session):
    expected = [
        Ports("ABC", "Root Region Port", "root"),
        Ports("DFG", "First Level Port", "first_level"),
    ]
    assert session.query(Ports).all() == expected


@dump_prices
def test_prices_mapper_can_load_prices(session):
    expected = [
        Prices("ABC", "DFG", "2022-05-06", 20),
        Prices("ABC", "DFG", "2023-04-05", 45),
    ]
    assert session.query(Prices).all() == expected


@dump_prices
def test_relationship_between_tables(session):

    result = session.execute(
        """
    SELECT r.slug, r.name, r.parent_slug
    FROM prices p
    JOIN ports po ON p.orig_code = po.code
    JOIN regions r ON po.parent_slug = r.slug
    WHERE p.orig_code = :orig_code
    AND p.dest_code = :dest_code
    AND r.slug = :slug ;
    """,
        dict(orig_code="ABC", dest_code="DFG", slug="root"),
    )

    assert Regions(*result.fetchone()) == Regions("root", "root region", None)
