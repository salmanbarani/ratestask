from sqlalchemy import Table, MetaData, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import mapper

from src.ratestack.domain import models

metadata = MetaData()

regions = Table(
    "regions",
    metadata,
    Column("slug", String, primary_key=True),
    Column("name", String(255), nullable=False),
    Column("parent_slug", ForeignKey("regions.slug")),

)

ports = Table(
    "ports",
    metadata,
    Column("code", String(5), primary_key=True),
    Column("name", String(2555), nullable=True),
    Column("parent_slug", ForeignKey("regions.slug")),
)

prices = Table(
    "prices",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("orig_code", ForeignKey("ports.code")),
    Column("dest_code", ForeignKey("ports.code")),
    Column("price", Integer, nullable=False),
    Column("date", Date, nullable=True),
)


def start_mappers():
    mapper(models.Regions, regions)
    mapper(models.Ports, ports)
    mapper(models.Prices, prices)
