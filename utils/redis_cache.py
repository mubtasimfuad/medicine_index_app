import redis
import json
import logging
from typing import Any
import os

# Setup app and error loggers
app_logger = logging.getLogger("app_logger")
error_logger = logging.getLogger("error_logger")


class RedisCache:
    def __init__(self):
        # Construct Redis URL using environment variables with redis:// prefix
        redis_host = os.getenv("REDIS_HOST", "localhost")
        redis_port = os.getenv("REDIS_PORT", "6379")
        redis_url = f"redis://{redis_host}:{redis_port}/0"

        self.redis = redis.from_url(redis_url)

    def get(self, key: str) -> Any:
        try:
            raw_data = self.redis.get(key)
            if raw_data:
                app_logger.info(f"Cache hit for key: {key}")
                try:
                    return json.loads(raw_data)
                except (json.JSONDecodeError, TypeError):
                    app_logger.warning(
                        f"Non-JSON data retrieved from cache for key: {key}"
                    )
                    return raw_data
            app_logger.info(f"Cache miss for key: {key}")
            return None
        except redis.RedisError as e:
            error_logger.error(f"Redis get error for key '{key}': {e}")
            return None

    def set(self, key: str, value: Any, expiration: int = 3600):
        try:
            if isinstance(value, (dict, list)):
                json_value = json.dumps(value, default=str)
                self.redis.set(key, json_value, ex=expiration)
            else:
                self.redis.set(key, str(value), ex=expiration)
            app_logger.info(f"Set cache for key: {key} with expiration: {expiration}s")
        except redis.RedisError as e:
            error_logger.error(f"Redis set error for key '{key}': {e}")

    def delete(self, key: str):
        try:
            self.redis.delete(key)
            app_logger.info(f"Deleted cache for key: {key}")
        except redis.RedisError as e:
            error_logger.error(f"Redis delete error for key '{key}': {e}")

    def delete_pattern(self, pattern: str):
        try:
            for key in self.redis.scan_iter(match=pattern):
                self.redis.delete(key)
            app_logger.info(f"Deleted keys matching pattern: {pattern}")
        except redis.RedisError as e:
            error_logger.error(
                f"Redis delete pattern error for pattern '{pattern}': {e}"
            )

    # Lock acquisition
    def acquire_lock(self, lock_key: str, timeout: int = 10):
        """
        Acquire a lock for atomic operations.
        Returns the lock if acquired, None otherwise.
        """
        lock = self.redis.lock(lock_key, timeout=timeout)
        if lock.acquire(blocking=False):
            app_logger.info(f"Acquired lock on key: {lock_key}")
            return lock
        else:
            app_logger.warning(f"Failed to acquire lock on key: {lock_key}")
            return None

    # Lock release
    def release_lock(self, lock):
        """
        Release the given lock.
        """
        try:
            lock.release()
            app_logger.info("Released lock.")
        except redis.RedisError as e:
            error_logger.error(f"Error releasing lock: {e}")
