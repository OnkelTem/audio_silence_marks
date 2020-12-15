try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:
    # noinspection PyUnresolvedReferences
    import importlib_metadata

__version__ = importlib_metadata.version(__name__)
