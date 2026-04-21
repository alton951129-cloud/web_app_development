from app.models import get_db_connection

class Restaurant:
    @staticmethod
    def create(db_path, name, attraction_id, description, rating, image_url):
        conn = get_db_connection(db_path)
        cursor = conn.cursor()
        cursor.execute(
            '''INSERT INTO restaurant (name, attraction_id, description, rating, image_url)
               VALUES (?, ?, ?, ?, ?)''',
            (name, attraction_id, description, rating, image_url)
        )
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        return new_id

    @staticmethod
    def get_all(db_path):
        conn = get_db_connection(db_path)
        rows = conn.execute('SELECT * FROM restaurant ORDER BY id DESC').fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def get_by_id(db_path, restaurant_id):
        conn = get_db_connection(db_path)
        row = conn.execute('SELECT * FROM restaurant WHERE id = ?', (restaurant_id,)).fetchone()
        conn.close()
        return dict(row) if row else None
        
    @staticmethod
    def get_by_attraction_id(db_path, attraction_id):
        conn = get_db_connection(db_path)
        rows = conn.execute('SELECT * FROM restaurant WHERE attraction_id = ? ORDER BY rating DESC', (attraction_id,)).fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def update(db_path, restaurant_id, name, attraction_id, description, rating, image_url):
        conn = get_db_connection(db_path)
        conn.execute(
            '''UPDATE restaurant SET name = ?, attraction_id = ?, description = ?, rating = ?, image_url = ?
               WHERE id = ?''',
            (name, attraction_id, description, rating, image_url, restaurant_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def delete(db_path, restaurant_id):
        conn = get_db_connection(db_path)
        conn.execute('DELETE FROM restaurant WHERE id = ?', (restaurant_id,))
        conn.commit()
        conn.close()
