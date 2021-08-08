from flask import Flask, render_template, request, jsonify
from flask.json import jsonify
from googletrans import Translator
import sqlite3
import traceback
import sys
import json

app = Flask(__name__)
translator = Translator()
f = open("data.json")
data = json.load(f)

database_path = "translate_app.db"


def insert_data(path_db):

    try:
        conn = sqlite3.connect(path_db)
        cursor = conn.cursor()
        print("Successfully Connected to SQLite")

        # translate and insert new record
       
        raw_arr = data["data"]
        translations = translator.translate(raw_arr, dest="vi")
        for translation in translations:
            sqlite_insert_query = """INSERT INTO vocabulary
                    (original_text, google_translate, translated_text)  VALUES  (?, ?, ?)"""

            cursor.execute(
                sqlite_insert_query,
                (translation.origin, translation.text, translation.text),
            )

        conn.commit()
        print(
            "Record inserted successfully into vocabulary table ",
            cursor.rowcount,
        )
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table")
        print("Exception class is: ", error.__class__)
        print("Exception is", error.args)
        print("Printing detailed SQLite exception traceback: ")
        exc_type, exc_value, exc_tb = sys.exc_info()
        print(traceback.format_exception(exc_type, exc_value, exc_tb))
    finally:
        if conn:
            conn.close()
            print("The SQLite connection is closed")


def select_data(path_db):
    try:
        conn = sqlite3.connect(path_db, timeout=20)
        cursor = conn.cursor()
        print("Connected to SQLite")

        sqlite_select_query = """SELECT * from vocabulary"""
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()

        translations_arr = []
        for row in records:
            newItem = {
                "id": row[0],
                "origin": row[1],
                "google_translate": row[2],
                "translated_text": row[3],
            }
            translations_arr.append(newItem)

        cursor.close()
        return translations_arr

    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if conn:
            conn.close()
            print("The Sqlite connection is closed")

def update_data(item, path_db):
    try:
        conn = sqlite3.connect(path_db)
        cursor = conn.cursor()
        print("Connected to SQLite")

        sql_update_query = """UPDATE vocabulary SET translated_text = ? where original_text = ?"""
        cursor.execute(sql_update_query, (item["translated_text"], item["original_text"]))
        conn.commit()
        print(item["translated_text"], item["original_text"])
        print("Record Updated successfully ")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to update sqlite table", error)
    finally:
        if conn:
            conn.close()
            print("The SQLite connection is closed")

@app.route("/", methods=["GET", "POST"])
def main():
    # insert_data(database_path)
    translations_arr = []
    if request.method == "GET":
        translations_arr = select_data(database_path) != None and select_data(database_path) or []
        
    if request.method == "POST":
        data_from_form = request.get_json()
        update_data(data_from_form, database_path)
        # translations_arr = select_data(database_path) != None and select_data(database_path) or []

    return render_template("index.html", len_arr=len(translations_arr), translations_arr=translations_arr)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=3001)
