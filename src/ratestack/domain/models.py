from .utils import TypeChecker
from .exceptions import InvalidRegionException
from .types import Slug
from datetime import date
from decimal import Decimal
from abc import ABC, abstractmethod
from dataclasses import dataclass


class BaseModel(ABC):
    @abstractmethod
    def is_valid(self):
        raise NotImplementedError()


class Regions(BaseModel):
    def __init__(self, slug: Slug, name: str) -> None:
        self.slug = slug
        self.name = name
        self.parent_slug = set()  # type: set(Regions)

    def __repr__(self) -> str:
        return f"<Region {self.slug}"

    def __hash__(self):
        return hash(self.slug)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Regions):
            return False
        return other.slug == self.slug

    def is_valid(self):
        return TypeChecker.is_slug_valid(self.slug)

    def add_parent_region(self, region):
        if region.is_valid() and self != region:
            self.parent_slug.add(region)
        else:
            raise InvalidRegionException()


class Ports(BaseModel):
    def __init__(self, code: str, name: str, parent_slug: Slug) -> None:
        self.code = code
        self.name = name
        self.parent_slug = parent_slug

    def __repr__(self) -> str:
        return f"<Port {self.code}"

    def __str__(self) -> str:
        return str(self.code)

    def __hash__(self):
        return hash(self.code)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Ports):
            return False
        return other.code == self.code

    def is_valid(self):
        validators = [
            TypeChecker.is_code_valid(self.code),
            TypeChecker.is_slug_valid(self.parent_slug),
        ]

        return all(validators)


@dataclass(unsafe_hash=True)
class Prices(BaseModel):
    def __init__(self, origin_port: str, dest_port: str, date: date, price: Decimal) -> None:
        self.origin_port = origin_port
        self.dest_port = dest_port
        self.date = date
        self.price = price

    def is_valid(self):
        validators = [
            TypeChecker.is_code_valid(self.origin_port),
            TypeChecker.is_code_valid(self.dest_port),
            TypeChecker.is_price_valid(self.price),
            TypeChecker.is_date_valid(self.date)
        ]
        print(self.price)
        return all(validators)

    def __gt__(self, other):
        if self.date is None:
            return False
        if other.date is None:
            return True
        return self.date > other.date
