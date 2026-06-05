import json
from pathlib import Path

# Для демонстрации оставляем значения в коде. В реальном приложении стоит вынести в переменные окружения.
TERMS_MAP_PATH = "terms_map.json"
RAW_DOCUMENTS_DIRECTORY = "../knowledge_base"
DOCUMENTS_DIRECTORY = "raw_knowledge_base"


def replace(source: str, terms_map: dict[str, str]) -> str:
    for old, new in terms_map.items():
        source = source.replace(old, new)
    return source


def main():
    with open(TERMS_MAP_PATH, "r", encoding="utf-8") as f:
        terms_map = json.loads(f.read())

    for path in Path(RAW_DOCUMENTS_DIRECTORY).iterdir():
        file_name = replace(path.name.replace("_", " "), terms_map).replace(" ", "_")

        with open(path, "r", encoding="utf-8") as src:
            text = replace(src.read(), terms_map)

        with open(f"{DOCUMENTS_DIRECTORY}/{file_name}", "w", encoding="utf-8") as dst:
            dst.write(text)


if __name__ == "__main__":
    main()
