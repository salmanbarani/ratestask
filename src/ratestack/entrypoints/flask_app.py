

from flask import Flask, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ratestack import config
from ratestack.adapters import orm
from ratestack.adapters.exceptions import SQLEXECUTIONERROR
from ratestack.service_layer import services, unit_of_work

from .exceptions import InvalidQueryParamsError

orm.start_mappers()
get_session = sessionmaker(bind=create_engine(config.get_postgres_uri()))
app = Flask(__name__)


@app.route("/rates", methods=["GET"])
def get_rates():
    uow = unit_of_work.SqlAlchemyUnitOfWork()
    try:
        rates = services.get_price(uow, **request.args)
    except (InvalidQueryParamsError, SQLEXECUTIONERROR) as e:
        return {"message": str(e)}, 400

    result = [
        {
            "day": row[1].isoformat(),
            "average_price": float(row[0]) if row[0] is not None else "null",
        }
        for row in rates
    ]

    return {"rates": result}, 200
