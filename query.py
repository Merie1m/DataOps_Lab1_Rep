import sys

import duckdb

con = duckdb.connect("warehouse.duckdb", read_only=True)
relation = con.sql(sys.argv[1])
columns = list(relation.columns)
print(" | ".join(columns))
for row in relation.fetchall():
    print(" | ".join("" if value is None else str(value) for value in row))
