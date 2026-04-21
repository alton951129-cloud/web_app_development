import sqlite3

def get_db_connection(db_path="instance/database.db"):
    """
    獲取與 SQLite 的連接，並設定 row_factory。
    因為這是一個簡單的 db wrapper，這裡統一用這支 helper。
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn
