from prometheus_client import Counter, Histogram, Gauge, start_http_server
from config.settings import settings


# Metrics for the Tic-Tac-Toe application
class Metrics:
    """Prometheus metrics collection."""

    def __init__(self):
        # Game metrics
        self.games_created = Counter(
            "tictactoe_games_created_total", "Total games created"
        )
        self.moves_made = Counter(
            "tictactoe_moves_made_total", "Total moves made", ["player_type"]
        )
        self.games_won = Counter(
            "tictactoe_games_won_total", "Total games won", ["winner"]
        )
        self.games_quit = Counter("tictactoe_games_quit_total", "Total games quit")

        # AI metrics
        self.ai_move_duration = Histogram(
            "tictactoe_ai_move_duration_seconds", "Time taken for AI moves"
        )
        self.ai_cache_hits = Counter("tictactoe_ai_cache_hits_total", "AI cache hits")
        self.ai_cache_misses = Counter(
            "tictactoe_ai_cache_misses_total", "AI cache misses"
        )

        # Application metrics
        self.active_games = Gauge("tictactoe_active_games", "Number of active games")
        self.http_requests = Counter(
            "tictactoe_http_requests_total",
            "HTTP requests",
            ["method", "endpoint", "status"],
        )

    def start_metrics_server(self):
        """Start the Prometheus metrics HTTP server."""
        if settings.metrics_enabled:
            start_http_server(settings.metrics_port)

    def record_game_created(self):
        """Record a new game creation."""
        self.games_created.inc()
        self.active_games.inc()

    def record_move_made(self, player_type: str):
        """Record a move made by a player."""
        self.moves_made.labels(player_type=player_type).inc()

    def record_game_won(self, winner: str):
        """Record a game win."""
        self.games_won.labels(winner=winner).inc()
        self.active_games.dec()

    def record_game_quit(self):
        """Record a game quit."""
        self.games_quit.inc()
        self.active_games.dec()

    def record_ai_move_duration(self, duration: float):
        """Record AI move computation time."""
        self.ai_move_duration.observe(duration)

    def record_cache_hit(self):
        """Record an AI cache hit."""
        self.ai_cache_hits.inc()

    def record_cache_miss(self):
        """Record an AI cache miss."""
        self.ai_cache_misses.inc()

    def record_http_request(self, method: str, endpoint: str, status: int):
        """Record an HTTP request."""
        self.http_requests.labels(method=method, endpoint=endpoint, status=status).inc()


# Global metrics instance
metrics = Metrics()
