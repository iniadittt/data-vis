from flask import Flask, request, jsonify, render_template
from youtube import YoutubeCrawler
from flask_cors import CORS, cross_origin
from predict import nlp
import pandas as pd
import os

app = Flask(__name__, static_folder="static")
CORS(app, origins="*")

youtube = YoutubeCrawler()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/crawl", methods=["POST"])
def crawling():
    if request.method == "POST":
        video_id = request.form["video_id"]
        max_result = request.form["max_result"]

        results = youtube.crawl_comments(video_id=video_id, req_result=max_result)

        return render_template("index.html", table=results, show_results=bool(results))

    else:
        return (
            jsonify(
                {"status": {"code": 405, "message": "Method not allowed"}, "data": None}
            ),
            405,
        )


@app.route("/api/predict", methods=["POST"])
def prediction():
    if request.method == "POST":
        input_data = request.get_json()
        texts = input_data["texts"]  # Expecting a list of texts
        results = [nlp(text) for text in texts]

        return jsonify(
            {
                "status": {"code": 200, "message": "Succes predicting the sentiment"},
                "data": {"sentiments": results},
            }
        )

    else:
        return (
            jsonify(
                {"status": {"code": 405, "message": "Method not allowed"}, "data": None}
            ),
            405,
        )


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5001)))