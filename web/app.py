import os

from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

# อ่านค่าจาก Environment Variables
mongo_uri = os.environ.get("MONGO_URI")
db_name = os.environ.get("DB_NAME")

# เชื่อมต่อ MongoDB
client = MongoClient(mongo_uri)

# เลือก Database และ Collection
db = client[db_name]
collection = db["routers"]


@app.route("/")
def main():
    routers = list(collection.find())
    return render_template("index.html", data=routers)


@app.route("/add", methods=["POST"])
def add_router():
    ip = request.form.get("ip")
    username = request.form.get("username")
    password = request.form.get("password")

    if ip and username and password:
        collection.insert_one({"ip": ip, "username": username, "password": password})

    return redirect(url_for("main"))


@app.route("/delete", methods=["POST"])
def delete_router():
    router_id = request.form.get("id")

    if router_id:
        collection.delete_one({"_id": ObjectId(router_id)})

    return redirect(url_for("main"))


@app.route("/router/<router_ip>")
def router_detail(router_ip):

    routers = list(
        db["interface_status"].find({"router_ip": router_ip}).sort("timestamp", -1)
    )
    return render_template("router_detail.html", routers=routers, router_ip=router_ip)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
