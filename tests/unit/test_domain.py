import pytest
from ratestack.domain.exceptions import InvalidRegionException
from ratestack.domain.models import Regions, Ports, Prices
from datetime import date
from decimal import Decimal


def create_region(slug="slug_name", name="region name"):
    return Regions(slug, name)


def create_port(code="code", name="code name", parent_slug="parent_slug"):
    return Ports(code, name, parent_slug)


def create_price(orig_code="orcod", dest_code="dscod", date="2011-01-02", price=Decimal("50.0")):
    return Prices(
        orig_code=orig_code,
        dest_code=dest_code,
        price=price,
        date=date
    )


"""
        testing Regions
"""


def test_create_region():
    region_fields = {"slug": "special_slug", "name": "special slug name"}
    region = create_region(**region_fields)
    for key in region_fields.keys():
        assert region_fields[key] == getattr(region, key)


def test_parent_slug_is_empty():
    region = create_region()
    assert region.parent_slug is None


def test_invalid_slug_region_is_not_valid():
    invalid_region = create_region(slug="invalid slug")
    assert not invalid_region.is_valid()


def test_add_invalid_parent():
    child_region = create_region()
    invalid_region = create_region(
        slug="invalid slug", name="special slug name")
    with pytest.raises(InvalidRegionException):
        child_region.add_parent_region(invalid_region)


def test_can_not_add_the_same_region_as_parent_region():
    child_region = create_region()
    with pytest.raises(InvalidRegionException):
        child_region.add_parent_region(child_region)


def test_add_parent_sucessfully():
    child_region = create_region()
    parent_region = create_region(
        slug="slug", name="special slug name")

    child_region.add_parent_region(parent_region)

    assert child_region.parent_slug is parent_region
    assert parent_region.parent_slug is None


"""
            Testing Ports
"""


def test_create_port():
    port_fields = {"code": "asef", "name": "code name",
                   "parent_slug": "slug_name"}
    port = create_port(**port_fields)

    for key in port_fields.keys():
        assert port_fields[key] in getattr(port, key)


def test_more_than_5_code_char_is_invalid():
    invalid_port_fields = {"code": "more_than_five_code", "name": "code name",
                           "parent_slug": "slug_name"}
    invalid_port = create_port(**invalid_port_fields)

    assert not invalid_port.is_valid()


def test_not_valid_slug_port_is_invalid():
    invalid_port_fields = {"code": "valid", "name": "code name",
                           "parent_slug": "not slug"}
    invalid_port = create_port(**invalid_port_fields)

    assert not invalid_port.is_valid()


def test_port_is_valid():
    valid_port_fields = {"code": "valid", "name": "code name",
                         "parent_slug": "slug_name"}
    valid_port = create_port(**valid_port_fields)

    assert valid_port.is_valid()


"""
            Testing Prices
"""


def test_create_price():
    price_fields = {
        "orig_code": "orcod",
        "dest_code": "dscod",
        "price": Decimal("50.0"),
        "date": "2011-01-02"
    }
    price = create_price(**price_fields)

    for key in price_fields.keys():
        assert price_fields[key] == getattr(price, key)


def test_more_than_5_orig_code_is_invalid():
    prices = create_price(orig_code="ABCDEF", dest_code="XYZ",
                          date=date.today(), price=Decimal("100.00"))
    assert not prices.is_valid()


def test_more_than_5_destination_port_is_invalid():
    prices = create_price(orig_code="ABC", dest_code="XYDZZY",
                          date=date.today(), price=Decimal("100.00"))
    assert not prices.is_valid()


def test_price_negative_is_invalid():
    prices = create_price(orig_code="ABC", dest_code="XYZ",
                          date=date.today(), price=Decimal("-100.00"))
    assert not prices.is_valid()


def test_price_string_is_invalid():
    price = create_price(orig_code="ABC", dest_code="XYZ",
                         date=date.today(), price="not a decimal")
    assert not price.is_valid()


def test_not_valid_date_prices_is_invalid():
    prices = create_price(orig_code="ABC", dest_code="XYZ",
                          date="2022-15-01", price=Decimal("100.00"))
    assert not prices.is_valid()


def test_price_is_valid():
    prices = create_price(orig_code="ABC", dest_code="XYZ",
                          date="2022-12-23", price=Decimal("100.00"))
    assert prices.is_valid()
