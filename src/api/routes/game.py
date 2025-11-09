from flask import Blueprint, request
from flask_restx import Api, Resource, fields
from ..services.game_service import GameService
from ..models import AIConfig


# Create Blueprint and API
game_bp = Blueprint("game", __name__)
api = Api(
    game_bp,
    doc="/docs/",
    title="Tic-Tac-Toe API",
    version="1.0",
    description="A modern Tic-Tac-Toe game API with AI opponents",
)

# Initialize service
game_service = GameService()

# API Models for documentation
game_state_model = api.model(
    "GameState",
    {
        "board": fields.List(fields.List(fields.String), required=True),
        "current_player": fields.String(required=True),
        "mode": fields.String(required=False),
        "winner": fields.String(required=False),
        "is_full": fields.Boolean(required=True),
        "ai_thinking": fields.Boolean(required=False),
    },
)

move_request_model = api.model(
    "MoveRequest",
    {
        "row": fields.Integer(
            required=True, min=0, max=2, description="Row index (0-2)"
        ),
        "col": fields.Integer(
            required=True, min=0, max=2, description="Column index (0-2)"
        ),
    },
)

move_response_model = api.model(
    "MoveResponse",
    {
        "success": fields.Boolean(required=True),
        "message": fields.String(required=False),
        "game_state": fields.Nested(game_state_model, required=True),
    },
)

game_mode_model = api.model(
    "GameModeRequest",
    {
        "mode": fields.String(
            required=True, enum=["single", "two"], description="Game mode"
        )
    },
)

ai_config_model = api.model(
    "AIConfig",
    {
        "strategy_type": fields.String(
            required=True, enum=["random", "minimax"], description="AI strategy"
        ),
        "symbol": fields.String(
            required=True, enum=["X", "O"], description="AI symbol"
        ),
        "max_depth": fields.Integer(
            required=True, min=1, max=20, description="Max search depth for minimax"
        ),
    },
)


@api.route("/games")
class GameList(Resource):
    @api.doc("create_game")
    @api.expect(game_mode_model)
    @api.marshal_with(game_state_model)
    def post(self):
        """Create a new game."""
        try:
            data = request.get_json()
            if not data or "mode" not in data:
                api.abort(400, "Mode is required")

            mode = data["mode"]
            if mode not in ["single", "two"]:
                api.abort(400, 'Mode must be "single" or "two"')

            # Create AI config for single player mode
            ai_config = None
            if mode == "single":
                strategy_type = data.get("strategy_type", "minimax")
                symbol = data.get("symbol", "O")
                max_depth = data.get("max_depth", 9)

                ai_config = AIConfig(strategy_type, symbol, max_depth)

            game_id = game_service.create_new_game(mode, ai_config)
            game_state = game_service.get_game_state(game_id)

            return {"game_id": game_id, **game_state.__dict__}
        except Exception as e:
            api.abort(500, f"Internal server error: {str(e)}")


@api.route("/games/<string:game_id>")
class Game(Resource):
    @api.doc("get_game")
    @api.marshal_with(game_state_model)
    def get(self, game_id):
        """Get game state by ID."""
        game_state = game_service.get_game_state(game_id)
        if not game_state:
            api.abort(404, "Game not found")

        return {"game_id": game_id, **game_state.__dict__}

    @api.doc("reset_game")
    @api.marshal_with(game_state_model)
    def post(self, game_id):
        """Reset a game."""
        game_state = game_service.reset_game(game_id)
        if not game_state:
            api.abort(404, "Game not found")

        return {"game_id": game_id, **game_state.__dict__}

    @api.doc("quit_game")
    @api.marshal_with(game_state_model)
    def delete(self, game_id):
        """Quit a game (current player loses)."""
        game_state = game_service.quit_game(game_id)
        if not game_state:
            api.abort(404, "Game not found")

        return {"game_id": game_id, **game_state.__dict__}


@api.route("/games/<string:game_id>/moves")
class MoveList(Resource):
    @api.doc("make_move")
    @api.expect(move_request_model)
    @api.marshal_with(move_response_model)
    def post(self, game_id):
        """Make a move in the game."""
        try:
            data = request.get_json()
            if not data or "row" not in data or "col" not in data:
                api.abort(400, "Row and column are required")

            row = data["row"]
            col = data["col"]

            if not (0 <= row <= 2 and 0 <= col <= 2):
                api.abort(400, "Row and column must be between 0 and 2")

            result = game_service.make_move(game_id, row, col)

            return {
                "success": result.success,
                "message": result.message,
                "game_state": {**result.game_state.__dict__},
            }
        except Exception as e:
            api.abort(500, f"Internal server error: {str(e)}")


@api.route("/games/<string:game_id>/ai-move")
class AIMove(Resource):
    @api.doc("make_ai_move")
    @api.marshal_with(move_response_model)
    def post(self, game_id):
        """Make an AI move."""
        try:
            result = game_service.make_ai_move(game_id)

            return {
                "success": result.success,
                "message": result.message,
                "game_state": {**result.game_state.__dict__},
            }
        except Exception as e:
            api.abort(500, f"Internal server error: {str(e)}")
