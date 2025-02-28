from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Define five teams
teams = ["Team Alpha", "Team Beta", "Team Gamma", "Team Delta", "Team Epsilon"]

votes = {team: 0 for team in teams}  # Initialize votes for each team

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        team_name = request.form["team_name"]
        vote = request.form["vote"]

        if vote in teams and vote != team_name:  # Prevent self-voting
            votes[vote] += 1
        return redirect(url_for("results"))

    return render_template("index.html", teams=teams)

@app.route("/results")
def results():
    return render_template("results.html", votes=votes)

if __name__ == "__main__":
    app.run(debug=True)
