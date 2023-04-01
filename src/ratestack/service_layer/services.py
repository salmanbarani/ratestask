from ratestack.adapters.repository import AbstractRepository
from ratestack.service_layer import unit_of_work


def get_price(uow: unit_of_work.AbstractUnitOfWork, **kwargs):
    with uow:
        return uow.repo.get_price(**kwargs)
