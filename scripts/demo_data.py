#!/usr/bin/env python3
"""
demo_data.py
────────────
Genera datos sintéticos de clima para las 5 ciudades colombianas
y los carga en PostgreSQL. Útil para pruebas sin consumir la API.

Uso:
    python scripts/demo_data.py
"""
import sys
sys.path.insert(0, '.')

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from scripts.database import SessionLocal, create_all_tables
from scripts.models import Ciudad, RegistroClima

np.random.seed(42)

CIUDADES = [
    {"nombre": "Bogota",       "pais": "Colombia", "latitud": 4.60,  "longitud": -74.08, "temp_base": 14, "hum_base": 72},
    {"nombre": "Medellin",     "pais": "Colombia", "latitud": 6.29,  "longitud": -75.54, "temp_base": 22, "hum_base": 65},
    {"nombre": "Cali",         "pais": "Colombia", "latitud": 3.44,  "longitud": -76.52, "temp_base": 25, "hum_base": 70},
    {"nombre": "Barranquilla", "pais": "Colombia", "latitud": 10.96, "longitud": -74.80, "temp_base": 30, "hum_base": 62},
    {"nombre": "Cartagena",    "pais": "Colombia", "latitud": 10.40, "longitud": -75.51, "temp_base": 31, "hum_base": 64},
]

N_REGISTROS = 200  # registros por ciudad


def generar_registros(ciudad_info: dict, ciudad_id: int) -> list:
    registros = []
    fecha_base = datetime.now() - timedelta(days=N_REGISTROS)

    for i in range(N_REGISTROS):
        temp = round(ciudad_info["temp_base"] + np.random.normal(0, 2.5), 1)
        humedad = round(np.clip(ciudad_info["hum_base"] + np.random.normal(0, 8), 20, 100), 1)
        viento = round(np.abs(np.random.normal(15, 8)), 1)
        sensacion = round(temp - (0.1 * humedad) + np.random.normal(0, 1), 1)

        registros.append(RegistroClima(
            ciudad_id=ciudad_id,
            temperatura=temp,
            sensacion_termica=sensacion,
            humedad=humedad,
            velocidad_viento=viento,
            descripcion="Demo",
            codigo_tiempo=800,
            fecha_extraccion=fecha_base + timedelta(days=i),
        ))
    return registros


def main():
    create_all_tables()
    db = SessionLocal()

    try:
        total = 0
        for c in CIUDADES:
            ciudad = db.query(Ciudad).filter_by(nombre=c["nombre"]).first()
            if not ciudad:
                ciudad = Ciudad(
                    nombre=c["nombre"], pais=c["pais"],
                    latitud=c["latitud"], longitud=c["longitud"]
                )
                db.add(ciudad)
                db.flush()
                print(f"  Ciudad creada: {c['nombre']}")
            else:
                print(f"  Ciudad ya existe: {c['nombre']}")

            registros = generar_registros(c, ciudad.id)
            db.bulk_save_objects(registros)
            total += len(registros)

        db.commit()
        print(f"\n✅ {total} registros demo insertados correctamente")

    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
