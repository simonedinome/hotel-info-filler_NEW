from importlib import import_module


def load_schema(category: str):
    return import_module(f"schemas.{category}")
