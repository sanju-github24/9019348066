from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# Load votes from file
def load_votes():
    try:
        with open("static/data.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# Save votes to file
def save_votes(votes):
    with open("static/data.json", "w") as file:
        json.dump(votes, file)

@app.route("/", methods=["GET", "POST"])
def index():
    votes = load_votes()
    if request.method == "POST":
        team_name = request.form.get("team")  # Get the selected team
        if team_name not in votes:
            return "Invalid vote", 400  # Error if the team does not exist
        votes[team_name] += 1
        save_votes(votes)
        return jsonify({"message": "Vote recorded!"})
    return render_template("index.html", votes=votes)

@app.route("/results")
def results():
    votes = load_votes()
    return render_template("results.html", votes=votes)

if __name__ == "__main__":
    app.run(debug=True)

@app.route("/", methods=["GET", "POST"])
def index():
    votes = load_votes()
    if request.method == "POST":
        team_name = request.form.get("team")
        print("Received vote for:", team_name)  # Debugging line
        if team_name not in votes:
            return "Invalid vote", 400
        votes[team_name] += 1
        save_votes(votes)
        return jsonify({"message": "Vote recorded!"})
    return render_template("index.html", votes=votes)
@app.route("/results")
def results():
    secret_key = request.args.get("key")
    if secret_key != "admin123":  # Change "admin123" to your own key
        return "Access Denied", 403
    votes = load_votes()
    return render_template("results.html", votes=votes)
