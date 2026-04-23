import sys
import os

# agregar la raíz del proyecto al path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from scripts.database import engine, Base

# IMPORTAR MODELOS (esto registra las tablas)
import scripts.models

print("Tablas detectadas en metadata:")
print(Base.metadata.tables.keys())

print("Creando tablas en PostgreSQL...")

Base.metadata.create_all(bind=engine)

print("Tablas creadas correctamente")