import pandas as pd
from scripts.database import SessionLocal
from scripts.models import Ciudad, RegistroClima
from datetime import datetime


def cargar_csv_a_db(ruta_csv="data/clima.csv"):

    db = SessionLocal()

    try:
        df = pd.read_csv(ruta_csv)

        for _, row in df.iterrows():

            # Saltar filas con datos vacíos
            if pd.isna(row["temperatura"]) or pd.isna(row["humedad"]):
                continue

            ciudad = db.query(Ciudad).filter_by(nombre=row["ciudad"]).first()

            if not ciudad:
                ciudad = Ciudad(
                    nombre=row["ciudad"],
                    pais=row["pais"],
                    latitud=row["latitud"],
                    longitud=row["longitud"]
                )

                db.add(ciudad)
                db.commit()
                db.refresh(ciudad)

            registro = RegistroClima(
                ciudad_id=ciudad.id,
                temperatura=row["temperatura"],
                sensacion_termica=row["sensacion_termica"],
                humedad=row["humedad"],
                velocidad_viento=row["velocidad_viento"],
                descripcion=row["descripcion"],
                codigo_tiempo=row["codigo_tiempo"],
                fecha_extraccion=datetime.now()
            )

            db.add(registro)

        db.commit()

        print("✅ Datos cargados correctamente en PostgreSQL")

    except Exception as e:
        print("❌ Error cargando datos:", e)

    finally:
        db.close()


if __name__ == "__main__":
    cargar_csv_a_db()