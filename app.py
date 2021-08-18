import re
from flask import Flask, render_template, request
from googletrans import Translator
import sqlite3
import traceback
import sys
import json

app = Flask(__name__)
translator = Translator()
f = open("data.json")
data = json.load(f)

# database_path = "translate_app.db"
database_path = "collection.anki2"


def insert_data():

    try:
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        print("Successfully Connected to SQLite")

        # translate and insert new record

        raw_arr = data["data"]
        translations = translator.translate(raw_arr, src="fr", dest="vi")
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


def select_many_records(req):
    try:
        limit = ("per_page" in req and int(req["per_page"])) or 20
        page_number = ("page_number" in req and int(req["page_number"])) or 1
        offset = limit * (page_number - 1)

        conn = sqlite3.connect(database_path, timeout=20)
        cursor = conn.cursor()

        sqlite_rows_count = """SELECT COUNT(*) FROM notes"""
        cursor.execute(sqlite_rows_count)
        number_of_rows = cursor.fetchone()

        sqlite_select_query = """SELECT * FROM notes LIMIT ? OFFSET ?;"""
        cursor.execute(sqlite_select_query, (limit, offset))

        records = cursor.fetchall()
        translations_arr = []
        for row in records:
            item = list(row)
            newItem = {
                "id": item[0],
                "origin": item[7],
                "translated_text": item[11],
            }
            translations_arr.append(newItem)

        cursor.close()
        pagination = {
            "total": number_of_rows[0],
            "per_page": limit,
            "page_number": page_number,
        }
        return (
            json.dumps(
                {
                    "status": True,
                    "msg": "Lấy dữ liệu thành công",
                    "data": translations_arr,
                    "pagination": pagination,
                }
            ),
            200,
            {"ContentType": "application/json"},
        )
    except sqlite3.Error as error:
        print("Failed to update sqlite table", error)
        return (
            json.dumps(
                {
                    "status": False,
                    "msg": "Lấy dữ liệu không thành công",
                }
            ),
            400,
            {"ContentType": "application/json"},
        )

def select_one_record(req):
    try:
        _id = req["_id"]

        conn = sqlite3.connect(database_path, timeout=20)
        cursor = conn.cursor()

        sqlite_select_query = """SELECT * FROM notes WHERE id = ?"""
        cursor.execute(sqlite_select_query, ([_id]))

        record = cursor.fetchone()
        item = {
            "id": record[0],
            "origin": record[7],
            "translated_text": record[11],
        }

        cursor.close()

        return (
            json.dumps(
                {
                    "status": True,
                    "msg": "Lấy dữ liệu thành công",
                    "data": item,
                }
            ),
            200,
            {"ContentType": "application/json"},
        )
    except sqlite3.Error as error:
        print("Failed to update sqlite table", error)
        return (
            json.dumps(
                {
                    "status": False,
                    "msg": "Lấy dữ liệu không thành công",
                }
            ),
            400,
            {"ContentType": "application/json"},
        )


def update_data(req):
    try:
        _id = req["_id"]
        translated_text = req["translated_text"] or None

        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()

        sql_update_query = """UPDATE notes SET translate = ? WHERE id = ? """
        cursor.execute(sql_update_query, (translated_text, _id))
        conn.commit()
        cursor.close()

        return (
            json.dumps({"status": True, "msg": "Thêm dữ liệu thành công"}),
            200,
            {"ContentType": "application/json"},
        )

    except sqlite3.Error as error:
        print("Failed to update sqlite table", error)
        return (
            json.dumps({"status": False, "msg": "Thêm dữ liệu KHÔNG thành công"}),
            400,
            {"ContentType": "application/json"},
        )


@app.route("/")
def fetchAll():
    req = request.args.to_dict()
    res = select_many_records(req)
    return res


@app.route("/<int:_id>")
def fetchOne(_id):
    # req = request.get_json()
    req = {"_id": _id}
    response = select_one_record(req)
    return response
        
@app.route("/<int:_id>", methods=["PUT"])
def update(_id):
    # req = request.get_json()
    if request.method == "PUT":
        req = request.get_json()
        req["_id"] = _id
        res = update_data(req)
        return res


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=3001)
