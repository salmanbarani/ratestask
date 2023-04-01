from sqlalchemy import (Column, Date, ForeignKey, Integer, String,
                        Table)
from sqlalchemy.orm import registry

from ratestack.domain import models

mapper_registry = registry()

regions = Table(
    "regions",
    mapper_registry.metadata,
    Column("slug", String, primary_key=True),
    Column("name", String(255), nullable=False),
    Column("parent_slug", ForeignKey("regions.slug")),
)

ports = Table(
    "ports",
    mapper_registry.metadata,
    Column("code", String(5), primary_key=True),
    Column("name", String(2555), nullable=True),
    Column("parent_slug", ForeignKey("regions.slug")),
)

prices = Table(
    "prices",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("orig_code", ForeignKey("ports.code")),
    Column("dest_code", ForeignKey("ports.code")),
    Column("price", Integer, nullable=False),
    Column("date", Date, nullable=True),
)


def start_mappers():
    mapper_registry.map_imperatively(models.Regions, regions)
    mapper_registry.map_imperatively(models.Ports, ports)
    mapper_registry.map_imperatively(models.Prices, prices)
