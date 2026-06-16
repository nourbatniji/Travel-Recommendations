from flask import Flask, request, jsonify, render_template
from algorithm import run_recommendation

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.get_json()

    user_code  = data.get("user_code")
    budget     = data.get("budget")
    max_cities = data.get("max_cities")  # None if user left the field blank

    if user_code is None or budget is None:
        return jsonify({"error": "Please fill in at least User Code and Budget."})

    if budget <= 0:
        return jsonify({"error": "Budget must be greater than zero."})

    # if user left max_cities blank, use a large number so all cities are considered
    if max_cities is None or max_cities <= 0:
        max_cities = 9999

    result = run_recommendation(user_code, budget, max_cities)
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)