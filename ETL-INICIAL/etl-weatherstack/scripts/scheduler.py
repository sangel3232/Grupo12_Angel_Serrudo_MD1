import schedule
import time
import sys
import os

# Permite importar extractor correctamente
sys.path.append(os.path.dirname(__file__))

from extractor import WeatherstackExtractor

def ejecutar_etl():
    try:
        print("Ejecutando ETL...")
        extractor = WeatherstackExtractor()
        extractor.ejecutar_extraccion()
        print("ETL finalizado.\n")
    except Exception as e:
        print(f"Error en ejecución automática: {e}")

# Ejecutar cada 1 hora
schedule.every(1).hours.do(ejecutar_etl)

print("Scheduler iniciado. Ejecutará cada 1 hora...")
ejecutar_etl()
while True:
    schedule.run_pending()
    time.sleep(60)