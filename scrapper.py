from flask import Flask, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route("/quotes", methods=["GET"])
def get_quotes():
    try:
        url = "http://quotes.toscrape.com/"  # You can change this to any target site
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raises HTTPError for bad responses

        soup = BeautifulSoup(response.text, "html.parser")
        quotes_list = []

        for quote_block in soup.find_all("div", class_="quote"):
            text = quote_block.find("span", class_="text").get_text()
            author = quote_block.find("small", class_="author").get_text()
            quotes_list.append({"text": text, "author": author})

        return jsonify({"status": "success", "data": quotes_list})

    except requests.exceptions.RequestException as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    except Exception as e:
        return jsonify({"status": "error", "message": f"Unexpected error: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
