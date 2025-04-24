import hashlib
from diskcache import Cache

# 使用装饰器缓存函数结果
def cache_func(key="", expire=3600, cache_dir="cache_db"):
    # 创建持久化缓存，存储在cache_db目录
    cache = Cache(cache_dir)
    
    def decorator(func):
        def wrapper(*args, **kwargs):
            # 创建基于函数参数的哈希值作为缓存键
            args_str = str(args) + str(sorted(kwargs.items()))
            cache_key = (key + "_" if key else "") + hashlib.md5(args_str.encode()).hexdigest()
            # 尝试从缓存获取
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                return cached_result
            # 缓存未命中，执行函数
            result = func(*args, **kwargs)
            # 存储结果到缓存，过期时间1小时
            cache.set(cache_key, result, expire=expire)
            return result
        return wrapper
    return decorator


def cache_clear(cache_dir="cache_db"):
    cache = Cache(cache_dir)
    cache.clear()