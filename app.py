from flask import Flask, render_template, request, session
from utils import *

app = Flask(__name__)
app.config["SECRET_KEY"] = "sjdflkajdlkjasldjflakdh54fd5g64d65f4g6dfg46d5f4g65d"


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/urlchecker", methods=["POST"])
def urlchecker():
    if request.method == "POST":
        url = request.get_json()['url']
        urlchecker = checkURL(url)
        global final_data
        final_data = urlchecker["data"]
        return urlchecker

@app.route("/download", methods=["POST"])
def download():
    if request.method == "POST":
        user_option = request.get_json()['data']
        if final_data != "":
            print("final data: ", final_data)
            downloadFile(user_option, final_data)
            return "Download detected"
        else:
            return "Could't get the vid data!"

@app.route("/downloadProgress", methods=["GET"])
def downloadProgress():
    if request.method == "GET":
        download_progress_ = download_progress()
        if download_progress_ == 0:
            return {"status":0, "progress":download_progress_}
        elif download_progress_ > 0 and download_progress < 100:
            return {"status":1, "progress":download_progress_}
        elif download_progress_ == 100:
            return {"status":2, "progress":download_progress_}
        else:
            return {"status":3, "progress":download_progress_}
    else:
        return "Could't get the vid data!"

@app.route("/<path:webpage>", methods=["GET"])
def redirection(webpage):
    return "You are not allowed to be here!"

if __name__ == "__main__":
    app.run(debug=True)