from .db import get_db_connection
import sqlite3

# --- Itinerary (行程總表) ---

def get_all():
    """
    取得所有行程紀錄。
    回傳：行程字典列表。
    """
    conn = get_db_connection()
    try:
        itineraries = conn.execute('SELECT * FROM itinerary ORDER BY created_at DESC').fetchall()
        return [dict(row) for row in itineraries]
    except sqlite3.Error as e:
        print(f"Error fetching all itineraries: {e}")
        return []
    finally:
        conn.close()

def get_by_id(itinerary_id):
    """
    根據 ID 取得單一行程。
    參數：itinerary_id (int)
    回傳：行程字典或 None。
    """
    conn = get_db_connection()
    try:
        itinerary = conn.execute('SELECT * FROM itinerary WHERE id = ?', (itinerary_id,)).fetchone()
        return dict(itinerary) if itinerary else None
    except sqlite3.Error as e:
        print(f"Error fetching itinerary by id {itinerary_id}: {e}")
        return None
    finally:
        conn.close()

def create(data):
    """
    新增一筆行程紀錄。
    參數：data (dict) - 包含 title
    回傳：新紀錄的 ID 或 None。
    """
    conn = get_db_connection()
    try:
        cur = conn.execute('INSERT INTO itinerary (title) VALUES (?)', (data['title'],))
        conn.commit()
        return cur.lastrowid
    except sqlite3.Error as e:
        print(f"Error creating itinerary: {e}")
        return None
    finally:
        conn.close()

def update(itinerary_id, data):
    """
    更新指定 ID 的行程紀錄。
    參數：itinerary_id (int), data (dict)
    回傳：布林值代表是否成功。
    """
    conn = get_db_connection()
    try:
        conn.execute('UPDATE itinerary SET title = ? WHERE id = ?', (data['title'], itinerary_id))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error updating itinerary {itinerary_id}: {e}")
        return False
    finally:
        conn.close()

def delete(itinerary_id):
    """
    刪除指定 ID 的行程紀錄，並連同其下的行程項目一併刪除。
    參數：itinerary_id (int)
    回傳：布林值代表是否成功。
    """
    conn = get_db_connection()
    try:
        # 刪除關聯項目
        conn.execute('DELETE FROM itinerary_item WHERE itinerary_id = ?', (itinerary_id,))
        # 刪除行程主表
        conn.execute('DELETE FROM itinerary WHERE id = ?', (itinerary_id,))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error deleting itinerary {itinerary_id}: {e}")
        return False
    finally:
        conn.close()

# --- Itinerary Items (行程項目) ---

def get_items(itinerary_id):
    """
    取得行程內的所有項目。
    參數：itinerary_id (int)
    回傳：行程項目字典列表。
    """
    conn = get_db_connection()
    try:
        items = conn.execute('SELECT * FROM itinerary_item WHERE itinerary_id = ? ORDER BY event_time ASC', (itinerary_id,)).fetchall()
        return [dict(row) for row in items]
    except sqlite3.Error as e:
        print(f"Error fetching items for itinerary {itinerary_id}: {e}")
        return []
    finally:
        conn.close()

def add_item(itinerary_id, data):
    """
    新增行程項目。
    參數：itinerary_id (int), data (dict) - 包含 item_type, item_id, event_time
    回傳：新紀錄的 ID 或 None。
    """
    conn = get_db_connection()
    try:
        sql = 'INSERT INTO itinerary_item (itinerary_id, item_type, item_id, event_time) VALUES (?, ?, ?, ?)'
        cur = conn.execute(sql, (
            itinerary_id, 
            data['item_type'], 
            data['item_id'], 
            data['event_time']
        ))
        conn.commit()
        return cur.lastrowid
    except sqlite3.Error as e:
        print(f"Error adding item to itinerary {itinerary_id}: {e}")
        return None
    finally:
        conn.close()

def delete_item(item_id):
    """
    刪除指定 ID 的行程項目。
    參數：item_id (int)
    回傳：布林值代表是否成功。
    """
    conn = get_db_connection()
    try:
        conn.execute('DELETE FROM itinerary_item WHERE id = ?', (item_id,))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error deleting itinerary item {item_id}: {e}")
        return False
    finally:
        conn.close()
