from .db import get_db_connection
import sqlite3

def get_all():
    """
    取得所有景點紀錄。
    回傳：景點字典列表。
    """
    conn = get_db_connection()
    try:
        attractions = conn.execute('SELECT * FROM attraction ORDER BY created_at DESC').fetchall()
        return [dict(row) for row in attractions]
    except sqlite3.Error as e:
        print(f"Error fetching all attractions: {e}")
        return []
    finally:
        conn.close()

def get_by_id(attraction_id):
    """
    根據 ID 取得單一景點。
    參數：attraction_id (int)
    回傳：景點字典或 None。
    """
    conn = get_db_connection()
    try:
        attraction = conn.execute('SELECT * FROM attraction WHERE id = ?', (attraction_id,)).fetchone()
        return dict(attraction) if attraction else None
    except sqlite3.Error as e:
        print(f"Error fetching attraction by id {attraction_id}: {e}")
        return None
    finally:
        conn.close()

def create(data):
    """
    新增一筆景點紀錄。
    參數：data (dict) - 包含 name, location, (optional) description, image_url
    回傳：新紀錄的 ID 或 None。
    """
    conn = get_db_connection()
    try:
        sql = 'INSERT INTO attraction (name, description, location, image_url) VALUES (?, ?, ?, ?)'
        cur = conn.execute(sql, (
            data['name'], 
            data.get('description'), 
            data['location'], 
            data.get('image_url')
        ))
        conn.commit()
        return cur.lastrowid
    except sqlite3.Error as e:
        print(f"Error creating attraction: {e}")
        return None
    finally:
        conn.close()

def update(attraction_id, data):
    """
    更新指定 ID 的景點紀錄。
    參數：attraction_id (int), data (dict)
    回傳：布林值代表是否成功。
    """
    conn = get_db_connection()
    try:
        sql = 'UPDATE attraction SET name = ?, description = ?, location = ?, image_url = ? WHERE id = ?'
        conn.execute(sql, (
            data['name'], 
            data.get('description'), 
            data['location'], 
            data.get('image_url'), 
            attraction_id
        ))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error updating attraction {attraction_id}: {e}")
        return False
    finally:
        conn.close()

def delete(attraction_id):
    """
    刪除指定 ID 的景點紀錄。
    參數：attraction_id (int)
    回傳：布林值代表是否成功。
    """
    conn = get_db_connection()
    try:
        conn.execute('DELETE FROM attraction WHERE id = ?', (attraction_id,))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error deleting attraction {attraction_id}: {e}")
        return False
    finally:
        conn.close()
