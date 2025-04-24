from .dependencies import ensure_dependencies
ensure_dependencies()  # 确保依赖已安装

from .logger import logger
from .cache import cache_func, cache_clear

__all__ = [
    "logger",
    "cache_func",
    "cache_clear",
    "ensure_dependencies",
]