from flask import Flask, render_template, request, jsonify, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "your_secret_key"  # For session management

votes = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/vote', methods=['POST'])
def vote():
    team_name = request.form.get('team')
    vote_for = request.form.get('vote_for')

    if team_name and vote_for and team_name != vote_for:
        votes[vote_for] = votes.get(vote_for, 0) + 1
        return jsonify({'message': 'Vote recorded successfully!'})
    return jsonify({'error': 'Invalid vote'}), 400

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == "admin123":  # Change this password!
            session['admin'] = True
            return redirect(url_for('admin_results'))
        return "Invalid password!", 403
    return render_template('admin_login.html')

@app.route('/admin/results')
def admin_results():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))  # Redirect if not logged in
    return render_template('results.html', votes=votes)

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/results')
def results():
    if not session.get("admin_logged_in"):  # Example condition
        return "Access Denied", 403
    return render_template('results.html', votes=votes)
