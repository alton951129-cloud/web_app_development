from flask import Blueprint, render_template, abort
from app.models import attraction, restaurant, itinerary

bp = Blueprint('places', __name__, url_prefix='/places')

@bp.route('/<int:id>')
def detail(id):
    """
    景點詳情頁面，包含天氣資訊。
    """
    attr = attraction.get_by_id(id)
    if not attr:
        abort(404)
    
    # 模擬天氣資訊
    weather_info = {
        'temp': 26,
        'condition': '舒適',
        'description': '適合旅遊的好天氣',
        'icon': '02d'
    }

    # 取得現有行程供使用者選擇
    plans = itinerary.get_all()
    
    return render_template('detail.html', attraction=attr, weather_info=weather_info, plans=plans)

@bp.route('/<int:id>/restaurants')
def restaurants(id):
    """
    景點周邊餐廳列表。
    """
    attr = attraction.get_by_id(id)
    if not attr:
        abort(404)
    
    rests = restaurant.get_by_attraction(id)
    return render_template('restaurants.html', attraction=attr, restaurants=rests)
