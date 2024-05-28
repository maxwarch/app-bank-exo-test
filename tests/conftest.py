from glob import glob


def refactor(string: str) -> str:
    return string.replace("/", ".").replace("\\", ".").replace(".py", "")

# permet d'importer tous les fichiers de fixture. Cela permet de "spécialiser" chaque fichier pour une meilleure lisibilité
pytest_plugins = [
    refactor(fixture) for fixture in glob("tests/fixtures/*.py") if "__" not in fixture
]
