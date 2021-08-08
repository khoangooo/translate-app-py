import sqlite3

try:
    sqliteConnection = sqlite3.connect("./flaskr/translate_app.db")
    sqlite_create_table_query = """CREATE TABLE IF NOT EXISTS vocabulary (
                                id INTEGER PRIMARY KEY ,
                                original_text TEXT,
                                google_translate TEXT,
                                translated_text TEXT,
                                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );"""

    cursor = sqliteConnection.cursor()
    print("Successfully Connected to SQLite")
    cursor.execute(sqlite_create_table_query)
    sqliteConnection.commit()
    print("SQLite table created")

    cursor.close()

except sqlite3.Error as error:
    print("Error while creating a sqlite table", error)
finally:
    if sqliteConnection:
        sqliteConnection.close()
        print("sqlite connection is closed")
