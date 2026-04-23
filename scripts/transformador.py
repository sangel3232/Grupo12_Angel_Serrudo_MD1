import pandas as pd
import logging
from datetime import datetime

logging.basicConfig(
<<<<<<< HEAD
    filename='logs/etl.log',
=======
    filename="../logs/etl.log",
>>>>>>> 241188abc411eb092c9a23228d311ed7b84787b6
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def transformar_datos():
    try:
        logging.info("Iniciando transformación de datos...")

<<<<<<< HEAD
        df = pd.read_csv('data/clima.csv')
=======
        df = pd.read_csv("../data/clima.csv")
>>>>>>> 241188abc411eb092c9a23228d311ed7b84787b6

        # Ejemplo de transformación
        df["temperatura_fahrenheit"] = (df["temperatura"] * 9/5) + 32
        df["fecha_transformacion"] = datetime.now()

<<<<<<< HEAD
        df.to_csv('data/clima_transformado.csv', index=False)
=======
        df.to_csv("../data/clima_transformado.csv", index=False)
>>>>>>> 241188abc411eb092c9a23228d311ed7b84787b6

        logging.info("Datos transformados correctamente.")
        print(" Transformación completada.")

    except Exception as e:
        logging.error(f"Error en transformación: {e}")
        print(" Error en transformación:", e)

if __name__ == "__main__":
    transformar_datos()