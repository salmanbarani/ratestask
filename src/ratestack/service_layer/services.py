from ratestack.adapters.repository import AbstractRepository


def get_price(session: any, repo: AbstractRepository, **kwargs):
    return repo.get_price(**kwargs)
