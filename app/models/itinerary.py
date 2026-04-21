from app.models import get_db_connection

class Itinerary:
    @staticmethod
    def create(db_path, title):
        conn = get_db_connection(db_path)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO itinerary (title) VALUES (?)', (title,))
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        return new_id

    @staticmethod
    def get_all(db_path):
        conn = get_db_connection(db_path)
        rows = conn.execute('SELECT * FROM itinerary ORDER BY id DESC').fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def get_by_id(db_path, itinerary_id):
        conn = get_db_connection(db_path)
        row = conn.execute('SELECT * FROM itinerary WHERE id = ?', (itinerary_id,)).fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def update(db_path, itinerary_id, title):
        conn = get_db_connection(db_path)
        conn.execute('UPDATE itinerary SET title = ? WHERE id = ?', (title, itinerary_id))
        conn.commit()
        conn.close()

    @staticmethod
    def delete(db_path, itinerary_id):
        conn = get_db_connection(db_path)
        conn.execute('DELETE FROM itinerary WHERE id = ?', (itinerary_id,))
        conn.commit()
        conn.close()

class ItineraryItem:
    @staticmethod
    def create(db_path, itinerary_id, item_type, item_id, event_time):
        conn = get_db_connection(db_path)
        cursor = conn.cursor()
        cursor.execute(
            '''INSERT INTO itinerary_item (itinerary_id, item_type, item_id, event_time)
               VALUES (?, ?, ?, ?)''',
            (itinerary_id, item_type, item_id, event_time)
        )
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        return new_id

    @staticmethod
    def get_by_itinerary_id(db_path, itinerary_id):
        conn = get_db_connection(db_path)
        # 用 JOIN 拉取名稱比較直覺，但因為多型關係，這裡先單純撈出清單給 Controller 處理邏輯
        rows = conn.execute('SELECT * FROM itinerary_item WHERE itinerary_id = ? ORDER BY event_time ASC', (itinerary_id,)).fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def delete(db_path, item_id):
        conn = get_db_connection(db_path)
        conn.execute('DELETE FROM itinerary_item WHERE id = ?', (item_id,))
        conn.commit()
        conn.close()
