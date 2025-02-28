from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Sample teams
teams = ["Team A", "Team B", "Team C", "Team D", "Team E"]
votes = {team: 0 for team in teams}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        team_name = request.form.get("team_name")
        vote = request.form.get("vote")
        
        if vote in teams and team_name and team_name != vote:
            votes[vote] += 1
            return render_template("thank_you.html")  # Show a thank you message instead of redirecting
        else:
            return "Invalid vote!", 400
    
    return render_template("index.html", teams=teams)

@app.route("/results")
def results():
    return render_template("results.html", votes=votes)

if __name__ == "__main__":
    app.run(debug=True)
