# utils/redis_cache.py

import redis
import json
import logging
from typing import Any
from datetime import datetime
import os


class RedisCache:
    def __init__(
        self, redis_url: str = os.getenv("REDIS_HOST", "redis://localhost:6379")
    ):
        self.redis = redis.from_url(redis_url)
        self.logger = logging.getLogger(__name__)

    def get(self, key: str) -> Any:
        try:
            raw_data = self.redis.get(key)
            if raw_data:
                try:
                    return json.loads(raw_data)
                except (json.JSONDecodeError, TypeError):
                    return raw_data
            return None
        except redis.RedisError as e:
            self.logger.error(f"Redis get error for key {key}: {e}")
            return None

    def set(self, key: str, value: Any, expiration: int = 3600):
        try:
            if isinstance(value, (dict, list)):
                json_value = json.dumps(value, default=str)
                self.redis.set(key, json_value, ex=expiration)
            else:
                self.redis.set(key, str(value), ex=expiration)
        except redis.RedisError as e:
            self.logger.error(f"Redis set error for key {key}: {e}")

    def delete(self, key: str):
        try:
            self.redis.delete(key)
        except redis.RedisError as e:
            self.logger.error(f"Redis delete error for key {key}: {e}")

    def delete_pattern(self, pattern: str):
        try:
            for key in self.redis.scan_iter(match=pattern):
                self.redis.delete(key)
            self.logger.info(f"Deleted keys matching pattern: {pattern}")
        except redis.RedisError as e:
            self.logger.error(f"Redis delete pattern error for pattern {pattern}: {e}")

    # Lock acquisition
    def acquire_lock(self, lock_key: str, timeout: int = 10):
        """
        Acquire a lock for atomic operations.
        Returns True if lock is acquired, False otherwise.
        """
        lock = self.redis.lock(lock_key, timeout=timeout)
        if lock.acquire(blocking=False):
            self.logger.info(f"Acquired lock on key: {lock_key}")
            return lock
        else:
            self.logger.warning(f"Failed to acquire lock on key: {lock_key}")
            return None

    # Lock release
    def release_lock(self, lock):
        """
        Release the given lock.
        """
        try:
            lock.release()
            self.logger.info(f"Released lock.")
        except redis.RedisError as e:
            self.logger.error(f"Error releasing lock: {e}")
