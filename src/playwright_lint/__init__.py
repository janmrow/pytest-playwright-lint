from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("pytest-playwright-lint")
except PackageNotFoundError:
    __version__ = "unknown"

__all__ = ["__version__"]
