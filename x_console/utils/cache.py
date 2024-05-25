import os, json, time
from pathlib import Path

class Cache:
    def __init__(self, directory=None):
        """Initialize the cache object with a directory.

        Args:
            directory (str, optional): Directory to store the cache file. If not provided, defaults to ~/.m.
        """
        if directory is None:
            # Default to ~/.m directory
            directory = os.path.join(Path.home(), ".junior")
        else:
            # Use the provided directory
            directory = Path(directory)

        # Ensure the cache directory exists
        os.makedirs(directory, exist_ok=True)

        # Path to the cache file
        self.cache_file = os.path.join(directory, "cache.json")
        self.cache = self._load_cache()

    def _load_cache(self):
        """Load the cache from the JSON file or create a new empty cache."""
        if os.path.exists(self.cache_file):
            with open(self.cache_file, "r", encoding="utf-8") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return {}
        else:
            return {}

    def _save_cache(self):
        """Save the current cache to the JSON file."""
        with open(self.cache_file, "w", encoding="utf-8") as f:
            json.dump(self.cache, f, indent=4)

    def set(self, key, value, ttl=None):
        """Set a value in the cache with an optional TTL (Time-to-Live).

        Args:
            key (str): Key to store the value.
            value (any): Value to be stored.
            ttl (int, optional): Time-to-Live in seconds. If not provided, the value is stored indefinitely.
        """
        expire_time = time.time() + ttl if ttl else None
        self.cache[key] = {
            "value": value,
            "expire_time": expire_time
        }
        self._save_cache()

    def get(self, key):
        """Retrieve a value from the cache.

        Args:
            key (str): Key to retrieve the value.

        Returns:
            any: The value if present and not expired, else None.
        """
        if key in self.cache:
            cache_entry = self.cache[key]
            if cache_entry["expire_time"] is None or cache_entry["expire_time"] > time.time():
                return cache_entry["value"]
            else:
                del self.cache[key]
                self._save_cache()
        return None

    def delete(self, key):
        """Delete a key-value pair from the cache.

        Args:
            key (str): Key to delete.
        """
        if key in self.cache:
            del self.cache[key]
            self._save_cache()

    def clear(self):
        """Clear all cache entries."""
        self.cache = {}
        self._save_cache()

# Example Usage
if __name__ == "__main__":
    cache = Cache()

    # Store data with a TTL of 10 seconds
    cache.set("example", {"data": "test"}, ttl=10)

    # Retrieve the stored data
    value = cache.get("example")
    print(f"Cached Value (before expiration): {value}")

    # Wait for 11 seconds to test expiration
    time.sleep(11)

    value = cache.get("example")
    print(f"Cached Value (after expiration): {value}")
