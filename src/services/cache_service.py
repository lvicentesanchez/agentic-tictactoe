import json
import hashlib
from typing import Optional, Tuple, List


class AICache:
    """Cache service for AI move computations."""

    def __init__(self) -> None:
        self.cache_enabled = True
        self._cache = {}  # Simple in-memory cache for now
        # TODO: Replace with Redis when available

    def _get_board_key(self, board: List[List[str]], symbol: str) -> str:
        """Generate a cache key for the board state."""
        board_str = json.dumps(board, sort_keys=True)
        key_data = f"{board_str}:{symbol}"
        return hashlib.md5(key_data.encode()).hexdigest()

    def get_move(
        self, board: List[List[str]], symbol: str
    ) -> Optional[Tuple[int, int]]:
        """Get cached move for the given board state."""
        if not self.cache_enabled:
            return None

        key = self._get_board_key(board, symbol)
        cached_data = self._cache.get(key)

        if cached_data:
            return tuple(cached_data)

        return None

    def store_move(
        self, board: List[List[str]], symbol: str, move: Tuple[int, int]
    ) -> None:
        """Store a move in the cache."""
        if not self.cache_enabled:
            return

        key = self._get_board_key(board, symbol)
        self._cache[key] = list(move)

    def clear_cache(self) -> None:
        """Clear all cached moves."""
        self._cache.clear()

    def get_cache_stats(self) -> dict:
        """Get cache statistics."""
        return {"size": len(self._cache), "enabled": self.cache_enabled}


# Global cache instance
ai_cache = AICache()
