import os
from flask import Flask
from datetime import datetime, timedelta

app = Flask(__name__)
TIMEOUT = timedelta(hours=1)
cwd = os.getcwd()
app.config["UPLOAD_FOLDER"] = os.path.join(cwd, "broiderer-server/static/uploads")
app.config["CONVERTED_FOLDER"] = os.path.join(cwd, "broiderer-server/static/converted")


def delete_expired_files():
    now = datetime.now()
    for filename in os.listdir(app.config["UPLOAD_FOLDER"]):
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        creation_time = datetime.fromtimestamp(os.path.getctime(file_path))
        if now - creation_time > TIMEOUT:
            os.remove(file_path)
    for filename in os.listdir(app.config["CONVERTED_FOLDER"]):
        file_path = os.path.join(app.config["CONVERTED_FOLDER"], filename)
        creation_time = datetime.fromtimestamp(os.path.getctime(file_path))
        if now - creation_time > TIMEOUT:
            os.remove(file_path)


delete_expired_files()
