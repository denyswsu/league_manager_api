from functools import reduce


def log_db_queries(f):
    """
    Decorator to log sql queries and execution time for a function.
    Example output:

    --------------------------------------------------------------------------------
    db queries log for prepare_sites_daily_stats:

    TOTAL COUNT: 6
    TOTAL TIME:  0.727

    0.001:  SELECT......
    --------------------------------------------------------------------------------

    """
    from django.db import connection

    def new_f(*args, **kwargs):
        res = f(*args, **kwargs)
        print("-" * 80)
        print("db queries log for %s:\n" % f.__name__)
        print("TOTAL COUNT: %s" % len(connection.queries))
        print(
            "TOTAL TIME:  %s\n"
            % reduce(lambda x, y: x + float(y["time"]), connection.queries, 0.0)
        )
        for q in connection.queries:
            print("%s:  %s\n" % (q["time"], q["sql"]))
        print("-" * 80)
        return res

    return new_f
