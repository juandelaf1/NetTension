import duckdb

conn = duckdb.connect("data/processed/nettension.duckdb")
tables = conn.execute("SHOW TABLES").fetchall()
print("Tables:", tables)

for t in tables:
    print(f"\n--- {t[0]} ---")
    schema = conn.execute(f"DESCRIBE {t[0]}").fetchall()
    for s in schema:
        print(f"  {s[0]}: {s[1]}")

conn.close()
