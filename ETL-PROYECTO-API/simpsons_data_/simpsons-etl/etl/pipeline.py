from etl.extract import extract_characters, extract_episodes
from etl.transform import transform_characters, transform_episodes
from etl.load import load_csv, load_postgres


def run_pipeline():

    print("🚀 Iniciando pipeline")

    characters = extract_characters()
    episodes = extract_episodes()

    characters_clean = transform_characters(characters)
    episodes_clean = transform_episodes(episodes)

    load_csv(characters_clean, "characters")
    load_csv(episodes_clean, "episodes")

    load_postgres(characters_clean, "dim_characters")
    load_postgres(episodes_clean, "dim_episodes")

    print("✅ Pipeline terminado")


if __name__ == "__main__":
    run_pipeline()