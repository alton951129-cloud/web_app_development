from flask import Blueprint

main_bp = Blueprint('main', __name__)
places_bp = Blueprint('places', __name__)
plan_bp = Blueprint('plan', __name__)

from app.routes import main, places, plan
