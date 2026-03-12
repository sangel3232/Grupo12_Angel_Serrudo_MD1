import requests
import pandas as pd

BASE_URL = "https://thesimpsonsapi.com/api"


def extract_all(endpoint):

    url = f"{BASE_URL}/{endpoint}"
    all_data = []

    print(f"Extrayendo {endpoint}...")

    while url:

        response = requests.get(url)

        if response.status_code != 200:
            raise Exception("Error al conectar con la API")

        data = response.json()

        results = data["results"]

        all_data.extend(results)

        url = data["next"]

    df = pd.json_normalize(all_data)

    print(f"Total registros descargados: {len(df)}")

    return df


def extract_characters():

    return extract_all("characters")


def extract_episodes():

    return extract_all("episodes")