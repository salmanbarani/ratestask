from datetime import datetime
from flask import Flask, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json
from ratestack import config
from ratestack.adapters import orm, repository
from ratestack.service_layer import services
from .exceptions import InvalidQueryParamsError
from ratestack.adapters.exceptions import SQLEXECUTIONERROR

orm.start_mappers()
get_session = sessionmaker(bind=create_engine(config.get_postgres_uri()))
app = Flask(__name__)


@app.route("/rates", methods=["GET"])
def get_rates():
    session = get_session()
    repo = repository.SqlAlchemyRepository(session)
    try:
        rates = services.get_price(
            session, repo, **request.args)
    except (InvalidQueryParamsError, SQLEXECUTIONERROR) as e:
        return {"message": str(e)}, 400

    result = [{'day': row[1].isoformat(), 'average_price': float(row[0]) if row[0] is not None else "null"}
              for row in rates]

    return {"rates": result}, 200
