from app.models import get_db_connection

class Attraction:
    @staticmethod
    def create(db_path, name, description, location, image_url):
        conn = get_db_connection(db_path)
        cursor = conn.cursor()
        cursor.execute(
            '''INSERT INTO attraction (name, description, location, image_url)
               VALUES (?, ?, ?, ?)''',
            (name, description, location, image_url)
        )
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()
        return new_id

    @staticmethod
    def get_all(db_path):
        conn = get_db_connection(db_path)
        rows = conn.execute('SELECT * FROM attraction ORDER BY id DESC').fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def get_by_id(db_path, attraction_id):
        conn = get_db_connection(db_path)
        row = conn.execute('SELECT * FROM attraction WHERE id = ?', (attraction_id,)).fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def update(db_path, attraction_id, name, description, location, image_url):
        conn = get_db_connection(db_path)
        conn.execute(
            '''UPDATE attraction SET name = ?, description = ?, location = ?, image_url = ?
               WHERE id = ?''',
            (name, description, location, image_url, attraction_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def delete(db_path, attraction_id):
        conn = get_db_connection(db_path)
        conn.execute('DELETE FROM attraction WHERE id = ?', (attraction_id,))
        conn.commit()
        conn.close()
