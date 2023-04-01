import pytest

from ratestack.adapters.repository import FakeRepository
from ratestack.service_layer import services, unit_of_work

repo = FakeRepository(
    [(30.0, "2022-04-05"), (40.0, "2022-04-06"), (20.0, "2022-04-08")]
)


class FakeUnitOfWork(unit_of_work.AbstractUnitOfWork):
    def __init__(self):
        self.repo = FakeRepository([])
        self.committed = False

    def commit(self):
        self.committed = True

    def rollback(self):
        pass


def test_service_no_params_return_data_from_repository():
    uow = FakeUnitOfWork()
    result = services.get_price(uow)
    assert result == repo.get_price()


def test_service_valid_params_return_data_from_repository():
    uow = FakeUnitOfWork()
    kwargs = {"origin": "ASD", "date_to": "2022-03-20"}
    result = services.get_price(uow, **kwargs)
    assert result == repo.get_price()


def test_service_invalid_valid_params_doesnt_effect_returned_data():
    uow = FakeUnitOfWork()
    kwargs = {"originasdfa": "ASD", "date_taasdfo": "2022-03-20"}
    result = services.get_price(uow, **kwargs)
    assert result == repo.get_price()
