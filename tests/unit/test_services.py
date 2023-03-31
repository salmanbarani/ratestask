import pytest
from ratestack.adapters.repository import FakeRepository
from ratestack.service_layer import services

repo = FakeRepository(
    [(30.0, '2022-04-05'), (40.0, '2022-04-06'), (20.0, '2022-04-08')]
)


class FakeSession:
    """This session is tests only for writing to DB"""
    commit = False


def test_service_no_params_return_data_from_repository():
    session = FakeSession()
    result = services.get_price(session, repo)
    assert result == repo.get_price()


def test_service_valid_params_return_data_from_repository():
    session = FakeSession()
    kwargs = {"origin": "ASD", "date_to": "2022-03-20"}
    result = services.get_price(session, repo, **kwargs)
    assert result == repo.get_price()


def test_service_invalid_valid_params_doesnt_effect_returned_data():
    session = FakeSession()
    kwargs = {"originasdfa": "ASD", "date_taasdfo": "2022-03-20"}
    result = services.get_price(session, repo, **kwargs)
    assert result == repo.get_price()
