import sqlite3
import os

# 資料庫路徑
DATABASE = 'instance/database.db'

def get_db_connection():
    """
    建立與 SQLite 資料庫的連線。
    設定 row_factory 為 sqlite3.Row，讓查詢結果可以透過欄位名稱存取。
    """
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn
