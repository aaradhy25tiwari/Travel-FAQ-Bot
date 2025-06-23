import json
from flask import Flask, render_template, request, redirect, url_for, session, jsonify

app = Flask(__name__)
app.secret_key = 'travelpal_secret_key_123'

# Load FAQ data from external JSON file
def load_faq_data():
    with open('faq_data.json', 'r', encoding='utf-8') as f:
        return json.load(f)

# In-memory "database" for users
users = {}

@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('chat'))
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if not username or not email or not password:
            return "All fields are required", 400

        if email in users:
            return "Email already registered", 400

        users[email] = {'username': username, 'password': password}
        session['user'] = username
        return redirect(url_for('chat'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if email in users and users[email]['password'] == password:
            session['user'] = users[email]['username']
            return redirect(url_for('chat'))
        return "Invalid credentials", 401
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/get_faqs', methods=['POST'])
def get_faqs():
    data = request.json
    category = data.get('category')
    language = data.get('language')

    faq_data = load_faq_data()

    if category in faq_data and language in faq_data[category]:
        return jsonify(faq_data[category][language])
    return jsonify([])

@app.route('/chat')
def chat():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('chat.html', username=session['user'])

if __name__ == '__main__':
    app.run(debug=True)
