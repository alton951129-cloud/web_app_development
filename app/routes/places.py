from flask import render_template, request, redirect, url_for, abort
from app.routes import places_bp

@places_bp.route('/places/<int:id>')
def place_detail(id):
    """
    HTTP Method: GET
    景點詳情與天氣查詢：依據 ID 獲取景點資訊，並呼叫外部 API 拿到即時天氣。
    輸出：渲染 templates/detail.html
    錯誤：若找不到 ID 則 abort(404)
    """
    pass

@places_bp.route('/places/<int:id>/restaurants')
def place_restaurants(id):
    """
    HTTP Method: GET
    周邊餐廳列表：顯示屬於特定景點附近的主題推薦餐廳。
    輸出：渲染 templates/restaurants.html
    """
    pass
