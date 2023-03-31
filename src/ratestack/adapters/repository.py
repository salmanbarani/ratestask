import abc
from ratestack.domain import models
from .utils import QueryStringCreator
from .exceptions import SQLEXECUTIONERROR


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, model: models.BaseModel):
        raise NotImplementedError

    @abc.abstractmethod
    def get_regions(self, **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def get_ports(self,  **kwargs):
        raise NotImplementedError

    @abc.abstractmethod
    def get_price(self,  **kwargs):
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session, creator=None) -> None:
        self.session = session
        self.creator = QueryStringCreator(
            self.session) if creator is None else creator

    def add(self, model: models.BaseModel):
        """add works for all models"""
        self.session.add(model)

    def get_price(self, **kwargs) -> any:
        try:
            result = self.session.execute(
                self.creator.price_query_string_factory(**kwargs)
            )
            return result.fetchall()
        except Exception as e:
            raise SQLEXECUTIONERROR(message=str(e))

    def get_regions(self, **kwargs):
        """Not been implemented"""
        return super().get_regions(**kwargs)

    def get_ports(self, **kwargs):
        """Not been implemented"""
        return super().get_ports(**kwargs)


class FakeRepository(AbstractRepository):
    """
        This repository is only used for testing purpose
    """

    def __init__(self, data_to_return) -> None:
        self.data_to_return = data_to_return

    def add(self, model: models.BaseModel):
        raise NotImplementedError

    def get_price(self, **kwargs):
        self.data_to_return

    def get_ports(self, **kwargs):
        """Not been implemented"""
        return super().get_ports(**kwargs)

    def get_regions(self, **kwargs):
        """Not been implemented"""
        return super().get_regions(**kwargs)
