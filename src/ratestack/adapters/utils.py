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
        query = self.session.execute(query_string)
        result = "(" + \
            ",".join(f"'{port[0]}'" for port in query.fetchall()) + ")"
        return result if result != '()' else False

    def _get_price_query_statement(self, **kwargs):
        where_cs = []
        if "date_from" in kwargs:
            where_cs.append(f"date >= '{kwargs['date_from']}'")
        if "date_to" in kwargs:
            where_cs.append(f"date <= '{kwargs['date_to']}'")
        if "origin" in kwargs:
            port_codes = self._get_port_code(kwargs['origin'])
            if port_codes:
                where_cs.append(
                    f"orig_code IN {port_codes}")
        if "destination" in kwargs:
            port_codes = self._get_port_code(kwargs['destination'])
            if port_codes:
                where_cs.append(
                    f"dest_code IN {port_codes}")

        where_claus = " AND ".join(where_cs) if len(where_cs) > 0 else ""
        where_claus = "WHERE " + where_claus if where_claus else ""
        return (
            f"""
            SELECT 
            CASE 
                WHEN COUNT(*) < 3 THEN NULL 
                ELSE AVG(price) 
            END as avg_price,
            date
            FROM prices
            {where_claus}
            GROUP BY date
            ORDER BY date;
           """
        )

    def price_query_string_factory(self, **kwargs):
        return self._get_price_query_statement(**kwargs)

    def region_query_string_factory(**kwargs) -> str:
        return super(**kwargs)

    def port_query_string_factory(**kwargs) -> str:
        return super(**kwargs)
