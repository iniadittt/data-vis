from dotenv import dotenv_values


def get_secret_key():
    config = dotenv_values(".env")
    secret_key = config.get("SECRET_KEY")

    return secret_key
