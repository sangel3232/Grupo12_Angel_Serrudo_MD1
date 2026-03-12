import os
from config.database import engine


def load_csv(df, filename):

    os.makedirs("data", exist_ok=True)

    path = f"data/{filename}.csv"

    df.to_csv(path, index=False)

    print(f"CSV guardado en {path}")


def load_postgres(df, table):

    df.to_sql(
        table,
        engine,
        if_exists="replace",
        index=False
    )

    print(f"Tabla {table} cargada en PostgreSQL")