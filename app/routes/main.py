from flask import Blueprint, render_template, request
from app.models import attraction

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """首頁"""
    return render_template('index.html')

@bp.route('/search')
def search():
    """搜尋景點"""
    query = request.args.get('q', '')
    # 這裡目前簡化為取得所有景點，實際實作可增加關鍵字篩選
    attractions = attraction.get_all()
    
    # 簡單的關鍵字篩選 (純 Python 實現，未來可優化至 SQL)
    if query:
        attractions = [a for a in attractions if query.lower() in a['name'].lower() or query.lower() in a['location'].lower()]
        
    return render_template('search.html', attractions=attractions, query=query)
