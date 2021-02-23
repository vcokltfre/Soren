from yaml import safe_load

def load(file: str = "./config.yml") -> dict:
    with open(file, encoding="utf-8") as f:
        return safe_load(f)
