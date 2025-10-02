from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

DATABASE = 'expenses.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            note TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    return render_template('dashboard.html')

@app.route('/add-expense')
def add_expense_page():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    return render_template('add_expense.html')

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    try:
        conn = get_db()
        cursor = conn.cursor()
        password_hash = generate_password_hash(password)
        cursor.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)',
                      (username, password_hash))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Registration successful'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Username already exists'}), 409

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id, password_hash FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()

    if user and check_password_hash(user['password_hash'], password):
        session['user_id'] = user['id']
        session['username'] = username
        return jsonify({'message': 'Login successful', 'username': username}), 200

    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logout successful'}), 200

@app.route('/api/expenses', methods=['GET'])
def get_expenses():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, amount, category, date, note, created_at
        FROM expenses
        WHERE user_id = ?
        ORDER BY date DESC
    ''', (session['user_id'],))
    expenses = cursor.fetchall()
    conn.close()

    expenses_list = []
    for expense in expenses:
        expenses_list.append({
            'id': expense['id'],
            'amount': expense['amount'],
            'category': expense['category'],
            'date': expense['date'],
            'note': expense['note'],
            'created_at': expense['created_at']
        })

    return jsonify(expenses_list), 200

@app.route('/api/expenses', methods=['POST'])
def create_expense():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()
    amount = data.get('amount')
    category = data.get('category')
    date = data.get('date')
    note = data.get('note', '')

    if not amount or not category or not date:
        return jsonify({'error': 'Amount, category, and date are required'}), 400

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO expenses (user_id, amount, category, date, note)
        VALUES (?, ?, ?, ?, ?)
    ''', (session['user_id'], amount, category, date, note))
    conn.commit()
    expense_id = cursor.lastrowid
    conn.close()

    return jsonify({'message': 'Expense created', 'id': expense_id}), 201

@app.route('/api/expenses/<int:expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM expenses WHERE id = ? AND user_id = ?',
                  (expense_id, session['user_id']))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Expense deleted'}), 200

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('SELECT SUM(amount) as total FROM expenses WHERE user_id = ?',
                  (session['user_id'],))
    total = cursor.fetchone()['total'] or 0

    current_month = datetime.now().strftime('%Y-%m')
    cursor.execute('''
        SELECT SUM(amount) as monthly_total
        FROM expenses
        WHERE user_id = ? AND date LIKE ?
    ''', (session['user_id'], f'{current_month}%'))
    monthly_total = cursor.fetchone()['monthly_total'] or 0

    cursor.execute('''
        SELECT category, SUM(amount) as total
        FROM expenses
        WHERE user_id = ?
        GROUP BY category
    ''', (session['user_id'],))
    categories = cursor.fetchall()
    conn.close()

    category_data = [{'category': cat['category'], 'total': cat['total']} for cat in categories]

    return jsonify({
        'total': total,
        'monthly_total': monthly_total,
        'categories': category_data
    }), 200

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
