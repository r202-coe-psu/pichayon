def init_cache(app):
    from cachelib import MemcachedCache

    servers = app.config.get("MEMCACHED_SERVERS", ["127.0.0.1:11211"])
    if not servers:
        servers = ["localhost:11211"]

    prefix = app.config.get("MEMCACHED_PREFIX", "")
    app.cache = MemcachedCache(servers=servers, key_prefix=prefix)
