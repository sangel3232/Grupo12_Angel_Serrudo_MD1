def transform_characters(df):

    print("Transformando personajes...")

    characters = df[['id','name','gender','occupation','status']]

    characters.columns = [
        'character_id',
        'name',
        'gender',
        'occupation',
        'status'
    ]

    return characters


def transform_episodes(df):

    print("Transformando episodios...")

    return df
