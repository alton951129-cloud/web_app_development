from flask import render_template, request, redirect, url_for
from app.routes import main_bp

@main_bp.route('/')
def index():
    """
    HTTP Method: GET
    首頁：顯示搜尋框與首頁歡迎畫面。
    輸出：渲染 templates/index.html
    """
    pass

@main_bp.route('/search')
def search():
    """
    HTTP Method: GET
    搜尋景點：讀取 query parameter `q`，並回傳搜尋結果。
    輸出：渲染 templates/search.html
    """
    pass
