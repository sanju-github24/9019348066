import sqlite3
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Initialize Database
def init_db():
    conn = sqlite3.connect("votes.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS votes (
            team TEXT PRIMARY KEY,
            count INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

init_db()

# Function to record votes
def record_vote(team_name):
    conn = sqlite3.connect("votes.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT count FROM votes WHERE team=?", (team_name,))
    row = cursor.fetchone()
    
    if row:
        cursor.execute("UPDATE votes SET count = count + 1 WHERE team=?", (team_name,))
    else:
        cursor.execute("INSERT INTO votes (team, count) VALUES (?, ?)", (team_name, 1))
    
    conn.commit()
    conn.close()

# Function to get results
def get_results():
    conn = sqlite3.connect("votes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT team, count FROM votes")
    results = dict(cursor.fetchall())
    conn.close()
    return results

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/vote', methods=['POST'])
def vote():
    data = request.json
    team_name = data.get("team_name")
    voted_for = data.get("voted_for")

    if not team_name or not voted_for:
        return jsonify({"error": "Missing team name or vote"}), 400
    
    if team_name == voted_for:
        return jsonify({"error": "You cannot vote for your own team"}), 400
    
    # Record vote in database
    record_vote(voted_for)
    
    return jsonify({"message": "Vote recorded!"})

@app.route('/results', methods=['GET'])
def results():
    return jsonify(get_results())

if __name__ == '__main__':
    app.run(debug=True)
