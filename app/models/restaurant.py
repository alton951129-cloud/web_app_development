from .db import get_db_connection
import sqlite3

def get_all():
    """
    取得所有餐廳紀錄。
    回傳：餐廳字典列表。
    """
    conn = get_db_connection()
    try:
        restaurants = conn.execute('SELECT * FROM restaurant ORDER BY created_at DESC').fetchall()
        return [dict(row) for row in restaurants]
    except sqlite3.Error as e:
        print(f"Error fetching all restaurants: {e}")
        return []
    finally:
        conn.close()

def get_by_id(restaurant_id):
    """
    根據 ID 取得單一餐廳。
    參數：restaurant_id (int)
    回傳：餐廳字典或 None。
    """
    conn = get_db_connection()
    try:
        restaurant = conn.execute('SELECT * FROM restaurant WHERE id = ?', (restaurant_id,)).fetchone()
        return dict(restaurant) if restaurant else None
    except sqlite3.Error as e:
        print(f"Error fetching restaurant by id {restaurant_id}: {e}")
        return None
    finally:
        conn.close()

def get_by_attraction(attraction_id):
    """
    取得特定景點附近的餐廳。
    參數：attraction_id (int)
    回傳：餐廳字典列表。
    """
    conn = get_db_connection()
    try:
        restaurants = conn.execute('SELECT * FROM restaurant WHERE attraction_id = ?', (attraction_id,)).fetchall()
        return [dict(row) for row in restaurants]
    except sqlite3.Error as e:
        print(f"Error fetching restaurants for attraction {attraction_id}: {e}")
        return []
    finally:
        conn.close()

def create(data):
    """
    新增一筆餐廳紀錄。
    參數：data (dict) - 包含 name, (optional) attraction_id, description, rating, image_url
    回傳：新紀錄的 ID 或 None。
    """
    conn = get_db_connection()
    try:
        sql = 'INSERT INTO restaurant (name, attraction_id, description, rating, image_url) VALUES (?, ?, ?, ?, ?)'
        cur = conn.execute(sql, (
            data['name'], 
            data.get('attraction_id'), 
            data.get('description'), 
            data.get('rating'), 
            data.get('image_url')
        ))
        conn.commit()
        return cur.lastrowid
    except sqlite3.Error as e:
        print(f"Error creating restaurant: {e}")
        return None
    finally:
        conn.close()

def update(restaurant_id, data):
    """
    更新指定 ID 的餐廳紀錄。
    參數：restaurant_id (int), data (dict)
    回傳：布林值代表是否成功。
    """
    conn = get_db_connection()
    try:
        sql = 'UPDATE restaurant SET name = ?, attraction_id = ?, description = ?, rating = ?, image_url = ? WHERE id = ?'
        conn.execute(sql, (
            data['name'], 
            data.get('attraction_id'), 
            data.get('description'), 
            data.get('rating'), 
            data.get('image_url'), 
            restaurant_id
        ))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error updating restaurant {restaurant_id}: {e}")
        return False
    finally:
        conn.close()

def delete(restaurant_id):
    """
    刪除指定 ID 的餐廳紀錄。
    參數：restaurant_id (int)
    回傳：布林值代表是否成功。
    """
    conn = get_db_connection()
    try:
        conn.execute('DELETE FROM restaurant WHERE id = ?', (restaurant_id,))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error deleting restaurant {restaurant_id}: {e}")
        return False
    finally:
        conn.close()
