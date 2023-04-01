from datetime import date

from ratestack.domain.models import Ports, Prices, Regions
from ratestack.service_layer.unit_of_work import SqlAlchemyUnitOfWork
from tests.utils import dump_data


def test_uow_can_add_and_retrieve_data(session_factory):
    uow = SqlAlchemyUnitOfWork(session_factory=session_factory)
    region = Regions("SLUG_NAME", "Region Name", None)
    port = Ports("AME", "Port Name", "SLUG_NAME")
    price = Prices("AME", "AME", date.today(), 50)

    with uow:
        uow.repo.add(region)
        uow.repo.add(port)
        uow.repo.add(price)
        uow.commit()

    data = {"origin": "AME", "destination": "AME", "date_to": date.today()}

    with uow:
        result = uow.repo.get_price(**data)
        assert result == [(None, date.today().isoformat())]
