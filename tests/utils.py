
def dump_data(test_func):
    def wrapper(session):
        session.execute(
            "INSERT INTO regions (slug, name, parent_slug) VALUES "
            '("root", "root region", NULL),'
            '("first_level", "First Level", "root"),'
            '("second_level", "Second Level", "first_level")')
        session.execute(
            "INSERT INTO ports (code, name, parent_slug) VALUES "
            '("AA", "AA Port", "root"), ("BB", "BB Port", "root"),'
            '("CC", "CC Port", "root"), ("EE", "EE Port", "first_level"),'
            '("FF", "FF Port", "first_level"), ("GG", "GG Port", "first_level"),'
            '("DD", "DD Port", "second_level"),("QQ", "QQ Port", "second_level"),'
            '("MM", "MM Port", "second_level")')

        session.execute(
            "INSERT INTO prices (orig_code, dest_code, date, price) VALUES "
            '("AA", "BB", "2022-05-05", 10), ("AA", "BB", "2022-05-05", 10),'
            '("AA", "MM", "2022-05-06", 30), ("AA", "BB", "2022-05-06", 40),'
            '("BB", "CC", "2022-04-05", 20), ("BB", "CC", "2022-04-05", 40),'
            '("BB", "CC", "2022-04-08", 20), ("BB", "AA", "2022-04-06", 40)'
        )
        return test_func(session)
    return wrapper


def dump_regions(test_func):
    def wrapper(session):
        session.execute(
            "INSERT INTO regions (slug, name, parent_slug) VALUES "
            '("root", "root region", NULL),'
            '("first_level", "First Level", "root"),'
            '("second_level", "Second Level", "first_level")')
        return test_func(session)
    return wrapper


def dump_ports(test_func):
    def wrapper(session):
        session.execute(
            "INSERT INTO ports (code, name, parent_slug) VALUES "
            '("ABC", "Root Region Port", "root"),'
            '("DFG", "First Level Port", "first_level")'
        )
        dump_region_decorator = dump_regions(test_func)
        return dump_region_decorator(session)
    return wrapper


def dump_prices(test_func):
    def wrapper(session):
        session.execute(
            "INSERT INTO prices (orig_code, dest_code, date, price) VALUES "
            '("ABC", "DFG", "2022-05-06", 20),'
            '("ABC", "DFG", "2023-04-05", 45)'
        )
        dump_port_decorator = dump_ports(test_func)
        return dump_port_decorator(session)
    return wrapper
