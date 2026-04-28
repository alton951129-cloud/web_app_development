from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import itinerary, attraction, restaurant

bp = Blueprint('plan', __name__, url_prefix='/plan')

@bp.route('/')
def index():
    """行程列表"""
    plans = itinerary.get_all()
    return render_template('planner_list.html', plans=plans)

@bp.route('/new')
def new():
    """建立行程頁面"""
    return render_template('planner_new.html')

@bp.route('/create', methods=['POST'])
def create():
    """儲存新行程"""
    title = request.form.get('title')
    if not title:
        flash("請輸入行程名稱")
        return redirect(url_for('plan.new'))
    
    itin_id = itinerary.create({'title': title})
    if itin_id:
        flash("行程建立成功！")
        return redirect(url_for('plan.index'))
    else:
        flash("建立失敗，請稍後再試")
        return redirect(url_for('plan.new'))

@bp.route('/<int:itinerary_id>')
def detail(itinerary_id):
    """行程細項規劃"""
    plan = itinerary.get_by_id(itinerary_id)
    if not plan:
        flash("找不到該行程")
        return redirect(url_for('plan.index'))
    
    items = itinerary.get_items(itinerary_id)
    
    # 補齊項目詳細資訊 (名稱)
    detailed_items = []
    for item in items:
        if item['item_type'] == 'attraction':
            detail_info = attraction.get_by_id(item['item_id'])
        else:
            detail_info = restaurant.get_by_id(item['item_id'])
        
        if detail_info:
            # 合併詳細資訊
            item_with_detail = dict(item)
            item_with_detail['name'] = detail_info['name']
            detailed_items.append(item_with_detail)
            
    return render_template('planner_detail.html', plan=plan, items=detailed_items)

@bp.route('/<int:itinerary_id>/items/add', methods=['POST'])
def add_item(itinerary_id):
    """新增項目至行程"""
    item_type = request.form.get('item_type')
    item_id = request.form.get('item_id')
    event_time = request.form.get('event_time')
    
    if not all([item_type, item_id, event_time]):
        flash("請填寫完整時間資訊")
        return redirect(request.referrer or url_for('plan.detail', itinerary_id=itinerary_id))
    
    itinerary.add_item(itinerary_id, {
        'item_type': item_type,
        'item_id': item_id,
        'event_time': event_time
    })
    
    flash("已成功加入行程清單")
    return redirect(url_for('plan.detail', itinerary_id=itinerary_id))

@bp.route('/<int:itinerary_id>/items/<int:item_id>/delete', methods=['POST'])
def delete_item(itinerary_id, item_id):
    """刪除行程項目"""
    if itinerary.delete_item(item_id):
        flash("已從清單移除項目")
    else:
        flash("移除失敗，請稍後再試")
    return redirect(url_for('plan.detail', itinerary_id=itinerary_id))

@bp.route('/<int:itinerary_id>/delete', methods=['POST'])
def delete_plan(itinerary_id):
    """刪除整個行程"""
    if itinerary.delete(itinerary_id):
        flash("行程已刪除")
    else:
        flash("刪除失敗")
    return redirect(url_for('plan.index'))
