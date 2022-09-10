import logging

from flask import Blueprint

logger = logging.getLogger(__name__)
api_routes = Blueprint("api_routes", __name__)


@api_routes.route("/healthcheck")
def health() -> dict[str, str]:
    return {"healthcheck": "Zorak, Ready to conquer the world."}
