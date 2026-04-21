from flask import render_template, request, redirect, url_for, abort
from app.routes import plan_bp

@plan_bp.route('/plan')
def plan_list():
    """
    HTTP Method: GET
    行程列表：讀取該使用者建立的所有行程紀錄。
    輸出：渲染 templates/planner_list.html
    """
    pass

@plan_bp.route('/plan/new')
def plan_new():
    """
    HTTP Method: GET
    建立行程頁面：顯示供使用者輸入名稱的簡單表單。
    輸出：渲染 templates/planner_new.html
    """
    pass

@plan_bp.route('/plan/create', methods=['POST'])
def plan_create():
    """
    HTTP Method: POST
    儲存新行程：接收表單資料，寫入 DB。
    輸出：重導向至 /plan
    """
    pass

@plan_bp.route('/plan/<int:itinerary_id>')
def plan_detail(itinerary_id):
    """
    HTTP Method: GET
    行程明細：取得行程裡包含的所有景點與餐廳項目，並依照時間排序佈局。
    輸出：渲染 templates/planner_detail.html
    """
    pass

@plan_bp.route('/plan/<int:itinerary_id>/items/add', methods=['POST'])
def plan_add_item(itinerary_id):
    """
    HTTP Method: POST
    新增項目至行程：從景點頁面或餐廳頁面送出表單，將該筆資料附加上去。
    輸出：重導向回上一個頁面或 /plan/<itinerary_id>
    """
    pass

@plan_bp.route('/plan/<int:itinerary_id>/items/<int:item_id>/delete', methods=['POST'])
def plan_delete_item(itinerary_id, item_id):
    """
    HTTP Method: POST
    刪除行程項目：從行程表中將特定計畫剔除。
    輸出：重導向至 /plan/<itinerary_id>
    """
    pass
