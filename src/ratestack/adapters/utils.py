from abc import ABC, abstractmethod


class BaseCreator(ABC):
    @abstractmethod
    def region_query_string_factory(**kwargs) -> str:
        raise NotImplementedError

    @abstractmethod
    def port_query_string_factory(**kwargs) -> str:
        raise NotImplementedError

    @abstractmethod
    def price_query_string_factory(**kwargs) -> str:
        raise NotImplementedError


class QueryStringCreator(BaseCreator):
    def __init__(self, session) -> None:
        self.session = session

    def _get_port_code(self, code):
        query_string = f"SELECT code FROM ports WHERE code = '{code}' OR parent_slug = '{code}';"
        result = self.session.execute(query_string)
        return "(" + ",".join(f"'{port[0]}'" for port in result.fetchall()) + ")"

    def _get_price_query_statement(self, **kwargs):
        where_cs = []
        if "date_from" in kwargs:
            where_cs.append(f"date >= '{kwargs['date_from']}'")
        if "date_to" in kwargs:
            where_cs.append(f"date <= '{kwargs['date_to']}'")
        if "origin" in kwargs:
            where_cs.append(
                f"orig_code IN {self._get_port_code(kwargs['origin'])}")
        if "destination" in kwargs:
            where_cs.append(
                f"dest_code IN {self._get_port_code(kwargs['destination'])}")

        where_claus = " AND ".join(where_cs) if len(where_cs) > 0 else ""
        where_claus = "WHERE " + where_claus if where_claus else ""
        return (
            f'SELECT AVG(price), date FROM prices {where_claus}'
            ' GROUP BY date'
        )

    def price_query_string_factory(self, **kwargs):
        return self._get_price_query_statement(**kwargs)

    def region_query_string_factory(**kwargs) -> str:
        return super(**kwargs)

    def port_query_string_factory(**kwargs) -> str:
        return super(**kwargs)
