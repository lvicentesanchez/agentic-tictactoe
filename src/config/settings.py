import os


class Settings:
    """Application configuration settings."""

    def __init__(self) -> None:
        # Game settings
        self.board_size: int = int(os.getenv("TICTACTOE_BOARD_SIZE", "3"))
        self.ai_thinking_delay: int = int(
            os.getenv("TICTACTOE_AI_THINKING_DELAY", "1500")
        )
        self.ai_max_depth: int = int(os.getenv("TICTACTOE_AI_MAX_DEPTH", "9"))

        # Flask settings
        self.debug: bool = os.getenv("TICTACTOE_DEBUG", "False").lower() == "true"
        self.host: str = os.getenv("TICTACTOE_HOST", "127.0.0.1")
        self.port: int = int(os.getenv("TICTACTOE_PORT", "5000"))

        # Redis settings
        self.redis_url: str = os.getenv(
            "TICTACTOE_REDIS_URL", "redis://localhost:6379/0"
        )
        self.cache_timeout: int = int(os.getenv("TICTACTOE_CACHE_TIMEOUT", "3600"))

        # Logging settings
        self.log_level: str = os.getenv("TICTACTOE_LOG_LEVEL", "INFO")

        # Metrics settings
        self.metrics_enabled: bool = (
            os.getenv("TICTACTOE_METRICS_ENABLED", "True").lower() == "true"
        )
        self.metrics_port: int = int(os.getenv("TICTACTOE_METRICS_PORT", "8000"))


# Global settings instance
settings = Settings()
