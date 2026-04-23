<<<<<<< HEAD
# ETL Weatherstack - Extracción de Datos de Clima

Proyecto de Minería de Datos que implementa un pipeline ETL completo para 
extraer, transformar y cargar datos de clima usando Weatherstack API.

##  Objetivo

Aprender las 4 fases de un proceso ETL profesional:
1. **Extract** - Obtener datos de APIs externas
2. **Transform** - Procesar y normalizar datos
3. **Load** - Almacenar en múltiples formatos
4. **Visualize** - Analizar y presentar resultados

##  Quick Start

### Requisitos
- Python 3.11+
- pip
- Git

### Instalación

```bash
# Clonar repositorio
git clone https://github.com/sangel3232/Grupo12_Angel_Serrudo_MD1.git
cd ETL-INICIAL/etl-weatherstack


# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # En Windows: .\venv\Scripts\Activate.ps1

# Instalar dependencias
pip install -r requirements.txt

# Configurar API key
echo "API_KEY=" > .env
```

### Ejecutar el Pipeline

```bash
python scripts/extractor.py
```

##  Salida del Pipeline

El script genera:
- `data/clima.csv` - Datos en formato CSV
- `data/clima_raw.json` - Datos en formato JSON
- `data/clima_analysis.png` - Gráficas de análisis
- `logs/etl.log` - Registro de ejecución
## ✅ Evidencia de ejecución

Ejecutado el: 2026-03-01

Se generaron correctamente:
- data/clima_raw.json
- data/clima.csv
- data/clima_analysis.png
- logs/etl.log

##  Estructura del Proyecto

```
etl-weatherstack/
├── scripts/
│   ├── extractor.py      # Extrae datos de la API
│   ├── transformador.py  # Procesa los datos
│   └── visualizador.py   # Genera gráficas
├── data/                 # Salida (CSV, JSON, PNG)
├── logs/                 # Registros de ejecución
├── .env                  # Variables de entorno (no commitear)
├── requirements.txt      # Dependencias Python
└── README.md            # Este archivo
```

##  Obtener API Key

1. Ve a [weatherstack.com](https://weatherstack.com)
2. Registrate y verifica tu email
3. En el dashboard, copia tu Access Key
4. Pega en `.env` como `API_KEY=tu_clave`

##  Conceptos Aprendidos

- **ETL Pipeline**: Ciclo de vida completo de datos
- **APIs REST**: Consumir servicios web externos
- **Python Avanzado**: Logging, manejo de errores, env vars
- **Versionamiento**: Git y GitHub para colaboración
- **Análisis de Datos**: Pandas, Matplotlib, Visualización
- **Buenas Prácticas**: Docstring, type hints, testing

##  Tecnologías

- Python 3.11
- requests (HTTP client)
- pandas (Data processing)
- matplotlib (Visualization)
- python-dotenv (Environment variables)
- Git/GitHub (Version control)

##  Autor

Tu Nombre - Ingeniería de Sistemas - CORHUILA

##  Licencia

Este proyecto está bajo licencia MIT - ver LICENSE.md

##  Contribuciones

Si deseas mejorar este proyecto:
1. Haz fork del repositorio
2. Crea una rama para tu mejora
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

---
**Última actualización:** Febrero 2026
**Estado:** En desarrollo ✅
=======
# 🌦 ETL WeatherStack - Proyecto de Ingeniería de Datos

##  Descripción

Este proyecto implementa un proceso ETL (Extract, Transform, Load) utilizando la API de WeatherStack para obtener datos climáticos de diferentes ciudades de Colombia.

El sistema extrae información meteorológica en tiempo real, la transforma agregando nuevos cálculos y genera archivos estructurados para su análisis y visualización.

---

##  Arquitectura del Proyecto

El flujo ETL está compuesto por tres fases principales:

1. **Extract** → `extractor.py`
2. **Transform** → `transformador.py`
3. **Load / Visualización** → `visualizador.py`

---

## Estructura del Proyecto
>>>>>>> 241188abc411eb092c9a23228d311ed7b84787b6
